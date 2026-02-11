# -*- coding: utf-8 -*-
import os, sys, shutil, subprocess

def run_cmd(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def clean_build_dir(build_path):
    if os.path.exists(build_path):
        print(f"🧹 Cleaning build directory (preserving .rxt, variant.json): {build_path}")
        for item in os.listdir(build_path):
            if item.endswith(".rxt") or item == "variant.json":
                print(f"🔒 Preserving {item}")
                continue
            full = os.path.join(build_path, item)
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)

def clean_install_dir(install_path):
    if os.path.isfile(install_path):
        print(f"🧹 Removing install file: {install_path}")
        os.remove(install_path)
    elif os.path.isdir(install_path):
        print(f"🧹 Removing install directory: {install_path}")
        shutil.rmtree(install_path)

def copy_package_py(source_path, install_path):
    src = os.path.join(source_path, "package.py")
    dst = os.path.join(install_path, "package.py")
    if os.path.exists(src):
        shutil.copy(src, dst)

def build(source_path, build_path, install_path, targets):
    version = os.environ.get("REZ_BUILD_PROJECT_VERSION", "3.3.3")

    # 1) 빌드 디렉터리 정리
    clean_build_dir(build_path)

    # 2) variant 서브경로 구성 (imath-3.1.9 or imath-3.2.0)
    imath_ver = os.environ.get("REZ_IMATH_VERSION", "")
    variant_subpath = f"imath-{imath_ver}" if imath_ver else ""

    # 3) install override (서버 경로 + variant 하위 디렉터리)
    server_base = f"/core/Linux/APPZ/packages/openexr/{version}"
    if "install" in targets:
        variant_idx = int(os.environ.get("REZ_BUILD_VARIANT_INDEX", "0"))
        # 첫 번째 variant 빌드 시 기존 전체 폴더 클린업 (구버전 flat 구조 제거)
        if variant_idx == 0:
            clean_install_dir(server_base)
            os.makedirs(server_base, exist_ok=True)
        install_root = os.path.join(server_base, variant_subpath) if variant_subpath else server_base
        clean_install_dir(install_root)
    else:
        install_root = install_path

    # 3) OpenEXR 소스/빌드 디렉터리 준비
    openexr_src = os.path.join(source_path, f"source/openexr-{version}")
    if not os.path.isdir(openexr_src):
        raise FileNotFoundError(f"❌ 소스 디렉토리가 없습니다: {openexr_src}")
    print(f"✅ Source directory: {openexr_src}")

    openexr_build = os.path.join(build_path, "openexr")
    os.makedirs(openexr_build, exist_ok=True)

    # 4) 의존성 경로
    imath_root = os.environ.get("REZ_IMATH_ROOT", "")
    if not imath_root:
        raise RuntimeError("❌ REZ_IMATH_ROOT not set. imath must be in requires.")
    print(f"📦 Imath root: {imath_root}")

    # 5) CMake 구성
    cmake_cmd = (
        f"cmake {openexr_src} "
        f"-DCMAKE_INSTALL_PREFIX={install_root} "
        f"-DCMAKE_BUILD_TYPE=Release "
        f"-DBUILD_TESTING=OFF "
        f"-DOPENEXR_INSTALL_EXAMPLES=OFF "
        f"-DOPENEXR_BUILD_PYTHON=OFF "
        f"-DCMAKE_INSTALL_LIBDIR=lib64 "
        f"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE "
        f"-DCMAKE_INSTALL_RPATH=\"{install_root}/lib64;{imath_root}/lib64\" "
        f"-DCMAKE_PREFIX_PATH=\"{imath_root}\" "
        f"-DImath_DIR={imath_root}/lib64/cmake/Imath"
    )

    run_cmd(cmake_cmd, cwd=openexr_build)

    # 6) 빌드
    run_cmd("cmake --build . --parallel", cwd=openexr_build)

    # 7) 설치
    if "install" in targets:
        run_cmd("cmake --install .", cwd=openexr_build)

        pkg_base = f"/core/Linux/APPZ/packages/openexr/{version}"
        os.makedirs(pkg_base, exist_ok=True)
        copy_package_py(source_path, pkg_base)

        # 빌드 마커
        marker = os.path.join(build_path, "build.rxt")
        open(marker, "a").close()

    # variant.json 생성 (rez 패키지 등록에 필요)
    variant_json = os.path.join(build_path, "variant.json")
    with open(variant_json, "w") as f:
        f.write("{}\n")

    print(f"✅ openexr-{version} build & install completed: {install_root}")

if __name__ == "__main__":
    build(
        source_path    = os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path     = os.environ["REZ_BUILD_PATH"],
        install_path   = os.environ["REZ_BUILD_INSTALL_PATH"],
        targets        = sys.argv[1:],
    )
