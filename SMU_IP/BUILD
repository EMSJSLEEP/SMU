load("@mixfw_rules//:build_rules.bzl", "mixfw_py_library", "mixfw_py_test", "mixfw_component")


mixfw_py_library(
    name="py_lib",
    srcs=glob([
        "driver/ipcore/*.py",
        ],
    ),
    install_dir = "/mix/driver/cyg/common/",
    strip_prefix = "driver/",
    skip_init = True
)

mixfw_py_test(
    name = "py_lib_tests",
    test_srcs = glob(["driver/tests/*.py"]),
    data = [":py_lib",
            "@lynx_core//:py_lib"],
)

mixfw_component(
    name = "CYG_SMU",
    srcs = [":py_lib"],
    maintainer = "Cygia",
    description = None,
)

