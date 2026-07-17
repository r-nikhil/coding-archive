document.addEventListener('DOMContentLoaded', function() {
    // Fetch stats and update charts
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateActivityChart(data);
            updateResponseChart(data);
        });

    // Activity Chart
    function updateActivityChart(data) {
        const ctx = document.getElementById('activityChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Posts', 'Replies', 'Mentions'],
                datasets: [{
                    label: 'Count',
                    data: [
                        data.post_count,
                        data.reply_count,
                        data.mention_count
                    ],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Response Type Chart
    function updateResponseChart(data) {
        const ctx = document.getElementById('responseChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Text Responses', 'Image Responses'],
                datasets: [{
                    data: [
                        data.text_response_count,
                        data.image_response_count
                    ],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    }
});
