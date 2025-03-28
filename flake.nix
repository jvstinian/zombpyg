{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-24.05";
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
                        numpy gymnasium pygame
                      ];

                      # Not including "nativeCheckInputs" as there are no additional dependencies for testing
                      doCheck = true;
		      # Including pytestCheckHook in nativeCheckInputs to run pytest. 
                      # If needed, arguments can be passed to pytest using pytestFlagsArray.  
                      # Alternatively, checkPhase can be explicitly provided.
                      # See https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/python.section.md#using-pytestcheckhook 
                      # for more details.
                      nativeCheckInputs = with python-final; [
                        pytestCheckHook 
                      ];
                  };
              })
          ];
          # Trying the simpler approach described in the manual at 
          # https://nixos.org/manual/nixpkgs/unstable/#how-to-override-a-python-package-using-overlays
          python3 = prev.python3.override {
              packageOverrides = prev.lib.composeManyExtensions final.pythonPackagesOverlays;
          };

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
              gymnasium
              pygame
              zombpyg
          ];
    
          dev-python = pkgs.python3.withPackages dev-python-packages;
        in 
          rec {
            devShells = {
              default = pkgs.mkShell {
                buildInputs = with pkgs; [
                  dev-python
                ];
                shellHook = "export PS1='\\[\\e[1;34m\\]zombpyg-dev > \\[\\e[0m\\]'";
              };
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
