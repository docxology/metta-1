#!/usr/bin/env python3
"""
DAF Complete Setup Script

This script provides a complete, hands-off setup of the DAF framework
including all dependencies, configuration, and validation.

Usage:
    python setup.py [OPTIONS]

Options:
    --profile PROFILE     Setup profile (research, production, dev) [default: research]
    --non-interactive     Run without prompts
    --with-tests         Include comprehensive testing
    --validate           Run full validation after setup
    --quick              Quick setup with minimal validation
    --help               Show this help message
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from daf.core.logging import setup_logging
from scripts.install import DAFInstaller


def print_banner():
    """Print DAF setup banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    DAF (Distributed Agent Framework)        ║
║                                                              ║
║        Professional Metta AI fork for automated,            ║
║        configurable multi-agent RL simulations              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_success():
    """Print success message."""
    success = """
╔══════════════════════════════════════════════════════════════╗
║                      Setup Complete!                         ║
║                                                              ║
║  🎉 DAF is now ready to run experiments!                    ║
║                                                              ║
║  Quick Start Commands:                                       ║
║    daf run experiment configs/experiments/quick_test.yaml   ║
║    daf validate system                                       ║
║    daf info                                                  ║
║                                                              ║
║  Documentation: See README.md for detailed usage             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(success)


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(
        description="DAF Complete Setup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic research setup
  python setup.py --profile research

  # Production setup with validation
  python setup.py --profile production --with-tests --validate

  # Quick development setup
  python setup.py --profile dev --quick

  # Non-interactive installation
  python setup.py --non-interactive --profile research
        """,
    )

    parser.add_argument(
        "--profile",
        choices=["research", "production", "dev", "minimal"],
        default="research",
        help="Setup profile (default: research)",
    )
    parser.add_argument("--non-interactive", action="store_true", help="Run without user prompts")
    parser.add_argument("--with-tests", action="store_true", help="Include comprehensive testing")
    parser.add_argument("--validate", action="store_true", help="Run full validation after setup")
    parser.add_argument("--quick", action="store_true", help="Quick setup with minimal validation")

    args = parser.parse_args()

    # Setup logging
    log_level = "INFO"
    if args.quick:
        log_level = "WARNING"
    setup_logging(level=log_level)

    # Print banner
    print_banner()

    # Create installer with arguments
    installer_args = argparse.Namespace(
        profile=args.profile,
        config=None,
        clean=False,
        validate=args.validate or not args.quick,
        dev=args.profile == "dev",
        non_interactive=args.non_interactive,
        verbose=args.profile == "dev",
    )

    installer = DAFInstaller(installer_args)

    async def run_setup():
        try:
            print(f"🔧 Setting up DAF with profile: {args.profile}")
            print("=" * 60)

            # Phase 1: System validation
            print("🔍 Validating system requirements...")
            system_validator = installer.system_validator
            system_result = system_validator.validate_system()

            if not system_result.is_valid:
                print("❌ System validation failed:")
                for issue in system_result.issues:
                    print(f"  - {issue}")
                print("💡 Please fix these issues before continuing.")
                sys.exit(1)

            print("✅ System validation passed")

            # Phase 2: Install DAF
            print("\n📦 Installing DAF framework...")
            result = await installer.run()

            if result != 0:
                print(f"❌ Installation failed with exit code: {result}")
                sys.exit(result)

            print("✅ DAF installation completed")

            # Phase 3: Quick validation (if not already done)
            if args.quick and not args.validate:
                print("\n🔍 Running quick validation...")
                validator = installer.install_manager.validator
                env_result = await validator.validate_environment_setup()

                if not env_result.is_valid:
                    print("⚠️  Quick validation found issues:")
                    for issue in env_result.issues:
                        print(f"  - {issue}")
                    print("💡 Run 'daf validate system' for detailed diagnostics")
                else:
                    print("✅ Quick validation passed")

            # Success
            print_success()

        except KeyboardInterrupt:
            print("\n👋 Setup cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            if args.profile == "dev":
                import traceback

                print(traceback.format_exc())
            sys.exit(1)

    # Run setup
    asyncio.run(run_setup())


if __name__ == "__main__":
    main()
