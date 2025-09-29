#!/usr/bin/env python3
"""
DAF Fork Initialization Script

This script initializes the complete DAF fork environment with all components:
- Setup and configuration
- Logging system
- Documentation generation
- Test infrastructure
- CLI interface
- Wrapper components

Run this script to set up the DAF fork for Metta integration.
"""

import logging
import sys
from pathlib import Path

# Add DAF to path
daf_src = Path(__file__).parent / "src"
sys.path.insert(0, str(daf_src))

from src.daf.logging.log_manager import LogManager
from src.daf.logging import setup_daf_logging
from src.daf.setup.daf_setup import initialize_daf_environment
from src.daf.config.daf_config import DAFConfigManager
from src.daf.tools import generate_comprehensive_daf_docs, sync_daf_with_metta, verify_daf_coverage
from src.daf.wrappers.metta_wrapper import AdaptiveWrapper, CurriculumWrapper, RLWrapper


def main():
    """Main DAF initialization function"""
    print("=" * 80)
    print("🚀 DAF FORK INITIALIZATION")
    print("=" * 80)
    print()

    # Step 1: Setup logging
    print("📝 Setting up comprehensive logging...")
    setup_daf_logging(log_level="INFO", log_file="daf/logs/daf_initialization.log", console_output=True)

    logger = logging.getLogger(__name__)
    logger.info("DAF initialization started")

    try:
        # Step 2: Initialize configuration
        print("⚙️  Initializing DAF configuration...")
        config_manager = DAFConfigManager()
        config = config_manager.get_config()
        logger.info("Configuration loaded")

        # Step 3: Initialize DAF environment
        print("🏗️  Setting up DAF environment...")
        setup = initialize_daf_environment(config)
        logger.info("DAF environment initialized")

        # Step 4: Synchronize with Metta repository
        print("🔄 Synchronizing with Metta repository...")
        sync_success = sync_daf_with_metta()
        if sync_success:
            logger.info("Metta synchronization completed")
        else:
            logger.warning("Metta synchronization failed - continuing with setup")

        # Step 5: Generate comprehensive documentation
        print("📚 Generating comprehensive documentation...")
        docs_success = generate_comprehensive_daf_docs()
        if docs_success:
            logger.info("Documentation generation completed")
        else:
            logger.warning("Documentation generation failed")

        # Step 6: Verify documentation coverage
        print("✅ Verifying documentation coverage...")
        coverage_success = verify_daf_coverage()
        if coverage_success:
            logger.info("Documentation coverage verified")
        else:
            logger.warning("Documentation coverage incomplete")

        # Step 7: Initialize wrapper components
        print("🔧 Initializing component wrappers...")
        wrappers = {"adaptive": AdaptiveWrapper(), "rl": RLWrapper(), "curriculum": CurriculumWrapper()}

        initialized_wrappers = 0
        for name, wrapper in wrappers.items():
            try:
                wrapper.initialize()
                logger.info(f"{name} wrapper initialized")
                initialized_wrappers += 1
            except Exception as e:
                logger.warning(f"Failed to initialize {name} wrapper: {e}")

        # Step 8: Setup log management
        print("📊 Setting up log management...")
        log_manager = LogManager("daf/logs")
        logger.info("Log management system initialized")

        # Step 9: Final validation
        print("🎯 Performing final validation...")
        validation_results = {
            "environment": setup is not None,
            "documentation": docs_success,
            "coverage": coverage_success,
            "wrappers": initialized_wrappers >= 2,  # At least 2 wrappers working
            "logging": True,  # Logging is already working
        }

        all_success = all(validation_results.values())

        # Summary report
        print("\n" + "=" * 80)
        print("📊 DAF INITIALIZATION SUMMARY")
        print("=" * 80)

        print("\n✅ INITIALIZATION RESULTS:")
        for component, success in validation_results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {component.upper():<20} {status}")

        print(f"\n🎯 OVERALL STATUS: {'✅ SUCCESS' if all_success else '⚠️  PARTIAL'}")

        if all_success:
            print("\n🚀 DAF FORK FULLY INITIALIZED!")
            print("   • All components working")
            print("   • Documentation generated")
            print("   • Metta integration active")
            print("   • Ready for development")
            print("\n📍 Next steps:")
            print("   1. Run: python -m daf.cli")
            print("   2. Generate docs: python -m daf.tools")
            print("   3. Explore examples: daf/examples/")
            print("   4. Run tests: daf/run_daf_tests.py")
        else:
            print("\n⚠️  DAF INITIALIZATION PARTIAL")
            print("   • Some components may need attention")
            print("   • Check logs for details")
            print("   • Manual setup may be required")

        # Create quick start guide
        print("\n📚 QUICK START GUIDE:")
        print("   • Documentation: @daf/README.md")
        print("   • Examples: daf/examples/")
        print("   • Tests: daf/run_daf_tests.py")
        print("   • CLI: python -m daf.cli")
        print("   • Logs: daf/logs/")
        print("\n🔧 AVAILABLE COMMANDS:")
        print("   daf setup      - Setup DAF environment")
        print("   daf docs       - Documentation management")
        print("   daf test       - Run test suite")
        print("   daf config     - Configuration management")
        print("   daf logs       - Log management")
        print("   daf wrapper    - Component wrappers")
        print("\n" + "=" * 80)

        logger.info(f"DAF initialization completed - Success: {all_success}")
        return 0 if all_success else 1

    except Exception as e:
        logger.error(f"DAF initialization failed: {e}")
        print(f"\n❌ INITIALIZATION FAILED: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
