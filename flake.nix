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
    nixpkgs,
    systems,
    devenv,
    poetry2nix,
  } @ inputs: let
    forEachSystem = nixpkgs.lib.genAttrs (import systems);
  in {
    packages = forEachSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      poetry2nix' = poetry2nix.lib.mkPoetry2Nix {inherit pkgs;};
    in {
      default = self.packages.${system}.db;
      db = poetry2nix'.mkPoetryApplication {
        projectDir = self;
      };
    });

    devShells = forEachSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = devenv.lib.mkShell {
        inherit inputs pkgs;

        modules = [
          {
            packages = with pkgs; [git coreutils];

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
          }
        ];
      };
    });
  };
}
