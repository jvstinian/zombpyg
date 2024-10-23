{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-23.11";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };
  outputs = { nixpkgs, flake-utils, ... }: 
    let 
      python-zombpyg-overlay = final: prev: {
          pythonPackagesOverlays = (prev.pythonPackagesOverlays or [ ]) ++ [
              (python-final: python-prev: {
                  zombpyg = python-final.buildPythonPackage rec {
                      name = "zombpyg";

                      src = ./.;

                      # was previously using "dependencies" but the packages 
                      # didn't appear to propagate to the output package
                      propagatedBuildInputs = with python-final; [
                        numpy gym pygame
                      ];

                      # Not including "nativeCheckInputs" as there are no additional dependencies for testing
                      doCheck = true;
                  };
              })
          ];
          python3 = let
                  self = prev.python3.override {
                      inherit self;
                      packageOverrides = prev.lib.composeManyExtensions final.pythonPackagesOverlays;
                  }; 
              in self;

          python3Packages = final.python3.pkgs;
      };
    in 
      flake-utils.lib.eachDefaultSystem (system: 
        let 
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ python-zombpyg-overlay ];
          };

          dev-python-packages = ps: with ps; [
              numpy 
              gym 
              pygame
              zombpyg
          ];
    
          dev-python = pkgs.python3.withPackages dev-python-packages;
        in 
          rec {
            devShell = pkgs.mkShell {
              buildInputs = with pkgs; [
                dev-python
              ];
            };
            packages = {
              zombpyg = pkgs.python3Packages.zombpyg;
              default = pkgs.python3Packages.zombpyg;
            };
            apps.default = {
              type = "app";
              program = "${packages.zombpyg}/bin/zombpyg";
            };
          }
      ) // {
        overlays.default = python-zombpyg-overlay;
      };
}
