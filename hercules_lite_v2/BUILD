load("@mixfw_rules//:build_rules.bzl", "mixfw_py_library","mixfw_py_test", "mixfw_component", "mixfw_doxygen")

mixfw_py_library(
    name="py_lib",
    srcs=glob([
        "driver/module/*.py"
        ],
    ),
    install_dir = "/mix/driver/cyg/hercules_lite_v2/",
    strip_prefix = "driver",
    skip_init = True
)

mixfw_py_test(
    name = "py_lib_tests",
    test_srcs = glob(["driver/tests/*.py"]),
    data = [":py_lib", 
            "@mix_tools//:py_lib",
            "@cyg_core_driver//:py_lib",
            "@MIX_SMU_Lite_CYG//:py_lib",
            "@AD4134//:py_lib",
	        "@MCP4725//:py_lib",
            "@AD5522//:py_lib",
	        "@mixrpc//:py_lib",
            "@mixrpc//:constants",
	        "@mixrpc//:scripts",
            "@lynx_core//:py_lib",
            "@mix_module_base_driver//:py_lib"]
)

mixfw_component(
    name = "MIX_HERCULES_CYG",
    srcs = [":py_lib"],
    maintainer = "Cygia",
    description = None,
)

mixfw_doxygen(
    name="cygstalordii_api_docs",
    src=":cyg_starlordii"
)
