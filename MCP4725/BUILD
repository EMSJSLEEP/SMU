load("@mixfw_rules//:build_rules.bzl", "mixfw_py_library","mixfw_py_test", "mixfw_component", "mixfw_doxygen")

mixfw_py_library(
    name="py_lib",
    srcs=glob([
        "ic/*.py"
        ],
    ),
    install_dir = "/mix/driver/cyg/common/",
    strip_prefix = "driver",
    skip_init = True
)

mixfw_py_test(
    name = "py_lib_tests",
    test_srcs = glob(["ic/tests/*.py"]),
    data = [":py_lib", 
            "@cyg_core_driver//:py_lib",
	    "@mixrpc//:py_lib",
            "@mixrpc//:constants",
	    "@mixrpc//:scripts",
            "@lynx_core//:py_lib",
            "@mix_module_base_driver//:py_lib"]
)

mixfw_component(
    name = "MCP4725",
    srcs = [":py_lib"],
    maintainer = "Cygia",
    description = None,
)

mixfw_doxygen(
    name="mcp4725_api_docs",
    src=":cyg_mcp4725"
)
