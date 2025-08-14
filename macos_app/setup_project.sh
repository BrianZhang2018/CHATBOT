#!/bin/bash

echo "Setting up ChatbotApp Xcode project..."

# Create a new Xcode project using command line
mkdir -p ChatbotApp.xcodeproj

# Create the project structure
cat > ChatbotApp.xcodeproj/project.pbxproj << 'EOF'
// !$*UTF8*$!
{
	archiveVersion = 1;
	classes = {
	};
	objectVersion = 56;
	objects = {

/* Begin PBXBuildFile section */
		A1234567890123456789012A /* ChatbotApp.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789012B /* ChatbotApp.swift */; };
		A1234567890123456789012C /* ContentView.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789012D /* ContentView.swift */; };
		A1234567890123456789012E /* ChatMessage.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789012F /* ChatMessage.swift */; };
		A1234567890123456789013A /* ChatParameters.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789013B /* ChatParameters.swift */; };
		A1234567890123456789013C /* AppSettings.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789013D /* AppSettings.swift */; };
		A1234567890123456789013E /* ChatModel.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789013F /* ChatModel.swift */; };
		A1234567890123456789014A /* OllamaService.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789014B /* OllamaService.swift */; };
		A1234567890123456789014C /* SettingsService.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789014D /* SettingsService.swift */; };
		A1234567890123456789014E /* ChatView.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789014F /* ChatView.swift */; };
		A1234567890123456789015A /* MessageView.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789015B /* MessageView.swift */; };
		A1234567890123456789015C /* InputView.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789015D /* InputView.swift */; };
		A1234567890123456789015E /* ModelSelectorView.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789015F /* ModelSelectorView.swift */; };
		A1234567890123456789016A /* SettingsView.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789016B /* SettingsView.swift */; };
		A1234567890123456789016C /* Extensions.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789016D /* Extensions.swift */; };
		A1234567890123456789016E /* Constants.swift in Sources */ = {isa = PBXBuildFile; fileRef = A1234567890123456789016F /* Constants.swift */; };
/* End PBXBuildFile section */

/* Begin PBXFileReference section */
		A1234567890123456789012A /* ChatbotApp.app */ = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = ChatbotApp.app; sourceTree = BUILT_PRODUCTS_DIR; };
		A1234567890123456789012B /* ChatbotApp.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ChatbotApp.swift; sourceTree = "<group>"; };
		A1234567890123456789012D /* ContentView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ContentView.swift; sourceTree = "<group>"; };
		A1234567890123456789012F /* ChatMessage.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ChatMessage.swift; sourceTree = "<group>"; };
		A1234567890123456789013B /* ChatParameters.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ChatParameters.swift; sourceTree = "<group>"; };
		A1234567890123456789013D /* AppSettings.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AppSettings.swift; sourceTree = "<group>"; };
		A1234567890123456789013F /* ChatModel.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ChatModel.swift; sourceTree = "<group>"; };
		A1234567890123456789014B /* OllamaService.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = OllamaService.swift; sourceTree = "<group>"; };
		A1234567890123456789014D /* SettingsService.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = SettingsService.swift; sourceTree = "<group>"; };
		A1234567890123456789014F /* ChatView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ChatView.swift; sourceTree = "<group>"; };
		A1234567890123456789015B /* MessageView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = MessageView.swift; sourceTree = "<group>"; };
		A1234567890123456789015D /* InputView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = InputView.swift; sourceTree = "<group>"; };
		A1234567890123456789015F /* ModelSelectorView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ModelSelectorView.swift; sourceTree = "<group>"; };
		A1234567890123456789016B /* SettingsView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = SettingsView.swift; sourceTree = "<group>"; };
		A1234567890123456789016D /* Extensions.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Extensions.swift; sourceTree = "<group>"; };
		A1234567890123456789016F /* Constants.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Constants.swift; sourceTree = "<group>"; };
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		A1234567890123456789012G /* Frameworks */ = {
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		A1234567890123456789012H /* ChatbotApp */ = {
			isa = PBXGroup;
			children = (
				A1234567890123456789012B /* ChatbotApp.swift */,
				A1234567890123456789012I /* Models */,
				A1234567890123456789012J /* Views */,
				A1234567890123456789012K /* Services */,
				A1234567890123456789012L /* Utilities */,
			);
			path = ChatbotApp;
			sourceTree = "<group>";
		};
		A1234567890123456789012I /* Models */ = {
			isa = PBXGroup;
			children = (
				A1234567890123456789012F /* ChatMessage.swift */,
				A1234567890123456789013B /* ChatParameters.swift */,
				A1234567890123456789013D /* AppSettings.swift */,
				A1234567890123456789013F /* ChatModel.swift */,
			);
			path = Models;
			sourceTree = "<group>";
		};
		A1234567890123456789012J /* Views */ = {
			isa = PBXGroup;
			children = (
				A1234567890123456789012D /* ContentView.swift */,
				A1234567890123456789014F /* ChatView.swift */,
				A1234567890123456789015B /* MessageView.swift */,
				A1234567890123456789015D /* InputView.swift */,
				A1234567890123456789015F /* ModelSelectorView.swift */,
				A1234567890123456789016B /* SettingsView.swift */,
			);
			path = Views;
			sourceTree = "<group>";
		};
		A1234567890123456789012K /* Services */ = {
			isa = PBXGroup;
			children = (
				A1234567890123456789014B /* OllamaService.swift */,
				A1234567890123456789014D /* SettingsService.swift */,
			);
			path = Services;
			sourceTree = "<group>";
		};
		A1234567890123456789012L /* Utilities */ = {
			isa = PBXGroup;
			children = (
				A1234567890123456789016D /* Extensions.swift */,
				A1234567890123456789016F /* Constants.swift */,
			);
			path = Utilities;
			sourceTree = "<group>";
		};
		A1234567890123456789012M = {
			isa = PBXGroup;
			children = (
				A1234567890123456789012H /* ChatbotApp */,
				A1234567890123456789012N /* Products */,
			);
			sourceTree = "<group>";
		};
		A1234567890123456789012N /* Products */ = {
			isa = PBXGroup;
			children = (
				A1234567890123456789012A /* ChatbotApp.app */,
			);
			name = Products;
			sourceTree = "<group>";
		};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		A1234567890123456789012O /* ChatbotApp */ = {
			isa = PBXNativeTarget;
			buildConfigurationList = A1234567890123456789012P /* Build configuration list for PBXNativeTarget "ChatbotApp" */;
			buildPhases = (
				A1234567890123456789012Q /* Sources */,
				A1234567890123456789012G /* Frameworks */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = ChatbotApp;
			productName = ChatbotApp;
			productReference = A1234567890123456789012A /* ChatbotApp.app */;
			productType = "com.apple.product-type.application";
		};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		A1234567890123456789012R /* Project object */ = {
			isa = PBXProject;
			attributes = {
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1500;
				LastUpgradeCheck = 1500;
				TargetAttributes = {
					A1234567890123456789012O = {
						CreatedOnToolsVersion = 15.0;
					};
				};
			};
			buildConfigurationList = A1234567890123456789012S /* Build configuration list for PBXProject "ChatbotApp" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = A1234567890123456789012M;
			productRefGroup = A1234567890123456789012N /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				A1234567890123456789012O /* ChatbotApp */,
			);
		};
/* End PBXProject section */

/* Begin PBXSourcesBuildPhase section */
		A1234567890123456789012Q /* Sources */ = {
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				A1234567890123456789012C /* ContentView.swift in Sources */,
				A1234567890123456789012E /* ChatMessage.swift in Sources */,
				A1234567890123456789013A /* ChatParameters.swift in Sources */,
				A1234567890123456789013C /* AppSettings.swift in Sources */,
				A1234567890123456789013E /* ChatModel.swift in Sources */,
				A1234567890123456789014A /* OllamaService.swift in Sources */,
				A1234567890123456789014C /* SettingsService.swift in Sources */,
				A1234567890123456789014E /* ChatView.swift in Sources */,
				A1234567890123456789015A /* MessageView.swift in Sources */,
				A1234567890123456789015C /* InputView.swift in Sources */,
				A1234567890123456789015E /* ModelSelectorView.swift in Sources */,
				A1234567890123456789016A /* SettingsView.swift in Sources */,
				A1234567890123456789016C /* Extensions.swift in Sources */,
				A1234567890123456789016E /* Constants.swift in Sources */,
				A1234567890123456789012A /* ChatbotApp.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
		A1234567890123456789012T /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MACOSX_DEPLOYMENT_TARGET = 14.0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = macosx;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)";
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			};
			name = Debug;
		};
		A1234567890123456789012U /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MACOSX_DEPLOYMENT_TARGET = 14.0;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = macosx;
				SWIFT_COMPILATION_MODE = wholemodule;
			};
			name = Release;
		};
		A1234567890123456789012V /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				COMBINE_HIDPI_IMAGES = YES;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_ASSET_PATHS = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_NSHumanReadableCopyright = "";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/../Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.example.ChatbotApp;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
			};
			name = Debug;
		};
		A1234567890123456789012W /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				COMBINE_HIDPI_IMAGES = YES;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_ASSET_PATHS = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_NSHumanReadableCopyright = "";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/../Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.example.ChatbotApp;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
			};
			name = Release;
		};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		A1234567890123456789012P /* Build configuration list for PBXNativeTarget "ChatbotApp" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				A1234567890123456789012V /* Debug */,
				A1234567890123456789012W /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
		A1234567890123456789012S /* Build configuration list for PBXProject "ChatbotApp" */ = {
			isa = XCConfigurationList;
			buildConfigurationList = (
				A1234567890123456789012T /* Debug */,
				A1234567890123456789012U /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
/* End XCConfigurationList section */
	};
	rootObject = A1234567890123456789012R /* Project object */;
}
EOF

echo "Project file created successfully!"
echo ""
echo "Next steps:"
echo "1. Open Xcode"
echo "2. Go to File → Open..."
echo "3. Navigate to this directory and select 'ChatbotApp.xcodeproj'"
echo "4. Build and run the project (⌘+R)"
echo ""
echo "If you still get 'damaged' warnings:"
echo "1. Go to System Preferences → Security & Privacy"
echo "2. Click 'Allow Anyway' for the app"
echo "3. Or run: xattr -cr /path/to/ChatbotApp.app"
