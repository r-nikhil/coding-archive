import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
import hmac
import hashlib

class WebhookService:
    def __init__(self):
        self.webhook_config_file = "webhook_config.json"
        self.webhook_logs_dir = "webhook_logs"
        self._ensure_directories()
        self.webhooks = self._load_webhook_config()
        
    def _ensure_directories(self):
        """Ensure webhook directories exist"""
        if not os.path.exists(self.webhook_logs_dir):
            os.makedirs(self.webhook_logs_dir)
    
    def _load_webhook_config(self) -> Dict[str, Any]:
        """Load webhook configuration"""
        if os.path.exists(self.webhook_config_file):
            try:
                with open(self.webhook_config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading webhook config: {e}")
                return {"webhooks": []}
        return {"webhooks": []}
    
    def _save_webhook_config(self):
        """Save webhook configuration"""
        try:
            with open(self.webhook_config_file, 'w') as f:
                json.dump(self.webhooks, f, indent=2)
        except Exception as e:
            print(f"Error saving webhook config: {e}")
    
    def add_webhook(self, url: str, events: List[str], secret: str = None, name: str = None) -> str:
        """Add a new webhook"""
        webhook_id = f"webhook_{len(self.webhooks.get('webhooks', []))}"
        
        webhook = {
            "id": webhook_id,
            "name": name or webhook_id,
            "url": url,
            "events": events,
            "secret": secret,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "last_triggered": None,
            "success_count": 0,
            "failure_count": 0
        }
        
        if "webhooks" not in self.webhooks:
            self.webhooks["webhooks"] = []
        
        self.webhooks["webhooks"].append(webhook)
        self._save_webhook_config()
        
        return webhook_id
    
    def remove_webhook(self, webhook_id: str) -> bool:
        """Remove a webhook"""
        if "webhooks" not in self.webhooks:
            return False
        
        for i, webhook in enumerate(self.webhooks["webhooks"]):
            if webhook["id"] == webhook_id:
                del self.webhooks["webhooks"][i]
                self._save_webhook_config()
                return True
        
        return False
    
    def toggle_webhook(self, webhook_id: str, active: bool) -> bool:
        """Enable/disable a webhook"""
        if "webhooks" not in self.webhooks:
            return False
        
        for webhook in self.webhooks["webhooks"]:
            if webhook["id"] == webhook_id:
                webhook["active"] = active
                self._save_webhook_config()
                return True
        
        return False
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate HMAC signature for webhook payload"""
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _log_webhook_event(self, webhook_id: str, event: str, success: bool, response_code: int = None, error: str = None):
        """Log webhook event"""
        log_entry = {
            "webhook_id": webhook_id,
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "response_code": response_code,
            "error": error
        }
        
        log_file = os.path.join(self.webhook_logs_dir, f"{datetime.now().strftime('%Y-%m-%d')}.json")
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"Error logging webhook event: {e}")
    
    def trigger_webhook(self, event: str, payload: Dict[str, Any]):
        """Trigger webhooks for a specific event"""
        if "webhooks" not in self.webhooks:
            return
        
        for webhook in self.webhooks["webhooks"]:
            if not webhook["active"] or event not in webhook["events"]:
                continue
            
            try:
                # Prepare payload
                webhook_payload = {
                    "event": event,
                    "timestamp": datetime.now().isoformat(),
                    "data": payload
                }
                
                payload_str = json.dumps(webhook_payload)
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Nikhil-Chatbot-Webhook/1.0"
                }
                
                # Add signature if secret is provided
                if webhook.get("secret"):
                    signature = self._generate_signature(payload_str, webhook["secret"])
                    headers["X-Webhook-Signature"] = f"sha256={signature}"
                
                # Send webhook
                response = requests.post(
                    webhook["url"],
                    data=payload_str,
                    headers=headers,
                    timeout=10
                )
                
                # Update webhook stats
                webhook["last_triggered"] = datetime.now().isoformat()
                if response.status_code == 200:
                    webhook["success_count"] += 1
                    self._log_webhook_event(webhook["id"], event, True, response.status_code)
                else:
                    webhook["failure_count"] += 1
                    self._log_webhook_event(webhook["id"], event, False, response.status_code, f"HTTP {response.status_code}")
                
            except Exception as e:
                webhook["failure_count"] += 1
                self._log_webhook_event(webhook["id"], event, False, error=str(e))
                print(f"Error triggering webhook {webhook['id']}: {e}")
        
        self._save_webhook_config()
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """Get webhook statistics"""
        stats = {
            "total_webhooks": len(self.webhooks.get("webhooks", [])),
            "active_webhooks": 0,
            "total_triggers": 0,
            "success_rate": 0.0,
            "webhooks": []
        }
        
        total_success = 0
        total_attempts = 0
        
        for webhook in self.webhooks.get("webhooks", []):
            if webhook["active"]:
                stats["active_webhooks"] += 1
            
            webhook_attempts = webhook["success_count"] + webhook["failure_count"]
            total_attempts += webhook_attempts
            total_success += webhook["success_count"]
            
            webhook_stats = {
                "id": webhook["id"],
                "name": webhook["name"],
                "url": webhook["url"],
                "events": webhook["events"],
                "active": webhook["active"],
                "success_count": webhook["success_count"],
                "failure_count": webhook["failure_count"],
                "last_triggered": webhook["last_triggered"],
                "success_rate": (webhook["success_count"] / webhook_attempts * 100) if webhook_attempts > 0 else 0
            }
            
            stats["webhooks"].append(webhook_stats)
        
        stats["total_triggers"] = total_attempts
        if total_attempts > 0:
            stats["success_rate"] = (total_success / total_attempts) * 100
        
        return stats
    
    def get_webhook_logs(self, date: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get webhook logs for a specific date or today"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        log_file = os.path.join(self.webhook_logs_dir, f"{date}.json")
        
        if not os.path.exists(log_file):
            return []
        
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            # Sort by timestamp (newest first) and limit
            logs.sort(key=lambda x: x["timestamp"], reverse=True)
            return logs[:limit]
            
        except Exception as e:
            print(f"Error reading webhook logs: {e}")
            return []
    
    def is_healthy(self) -> bool:
        """Check if webhook service is healthy"""
        return os.path.exists(self.webhook_logs_dir) and os.path.isdir(self.webhook_logs_dir)