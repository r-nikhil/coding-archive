{pkgs}: {
  deps = [
    pkgs.unzipNLS
    pkgs.redis
    pkgs.openssl
    pkgs.postgresql
  ];
}
