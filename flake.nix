{
  description = "Database management tool for wizbattle";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = {
    self,
    flake-parts,
    poetry2nix,
    ...
  } @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;} {
      imports = [
        inputs.devenv.flakeModule
      ];

      systems = import inputs.systems;

      perSystem = {
        config,
        pkgs,
        system,
        ...
      }: let
        poetry2nix' = poetry2nix.lib.mkPoetry2Nix {inherit pkgs;};
      in {
        packages.default = poetry2nix'.mkPoetryApplication {
          projectDir = self;
          preferWheels = true;
        };

        devenv.shells.default = {
          packages = with pkgs; [
            config.packages.default
            git
            coreutils
          ];

          services.postgres = {
            enable = true;

            initialDatabases = [{name = "wizbattle";}];

            settings = {
              unix_socket_directories = "/tmp";
            };
          };

          languages = {
            nix.enable = true;
            python = {
              enable = true;
              poetry.enable = true;
            };
          };
        };
      };
    };
}
