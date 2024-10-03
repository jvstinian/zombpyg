{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-23.11";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };
  outputs = { nixpkgs, flake-utils, ... }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [ ];
      };

      zombpyg = pkgs.python3Packages.buildPythonPackage rec {
          name = "zombpyg";

          src = ./.;

          # was previously using "dependencies" but the packages 
	  # didn't appear to propagate to the output package
          propagatedBuildInputs = with pkgs.python3.pkgs; [
            numpy gym pygame
          ];

          # Not including "nativeCheckInputs" as there are no additional dependencies for testing
          doCheck = true;
      };
      dev-python-packages = ps: with ps; [
          numpy 
          gym 
          pygame
          zombpyg
      ];
      dev-python = pkgs.python3.withPackages dev-python-packages;
    in rec {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          dev-python
        ];
      };
      packages = {
        zombpyg = zombpyg;
        default = zombpyg;
      };
      apps.default = {
        type = "app";
        program = "${packages.zombpyg}/bin/zombpyg";
      };
    }
  );
}
