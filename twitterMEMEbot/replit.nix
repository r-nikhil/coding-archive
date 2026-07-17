
{ pkgs }: {
    deps = [
        pkgs.python39
        pkgs.firefox
        pkgs.geckodriver
        pkgs.chromium
        pkgs.chromedriver
    ];
}
