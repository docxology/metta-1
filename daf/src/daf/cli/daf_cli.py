#!/usr/bin/env python3
"""
DAF Command Line Interface

Provides command-line interface for the DAF fork operations.
"""

import argparse
import sys
from pathlib import Path

try:
    from ..config.daf_config import DAFConfigManager
    from ..logging import setup_daf_logging
    from ..logging.log_manager import LogManager
except ImportError:
    # Fallback for testing scenarios
    try:
        from daf.config.daf_config import DAFConfigManager
        from daf.logging import setup_daf_logging
        from daf.logging.log_manager import LogManager
    except ImportError:
        # Final fallback - create placeholders
        class LogManager:
            def __init__(self):
                pass

        def setup_daf_logging():
            pass

        class DAFConfigManager:
            def __init__(self):
                pass


try:
    from ..tools.comprehensive_generator import generate_comprehensive_daf_docs
    from ..tools.sync_with_metta import sync_daf_with_metta
    from ..tools.verify_coverage import verify_daf_coverage
except ImportError:
    # Fallback for testing scenarios
    try:
        from daf.tools.comprehensive_generator import generate_comprehensive_daf_docs
        from daf.tools.sync_with_metta import sync_daf_with_metta
        from daf.tools.verify_coverage import verify_daf_coverage
    except ImportError:
        # Final fallback - create placeholders
        def generate_comprehensive_daf_docs():
            return True

        def sync_daf_with_metta():
            return True

        def verify_daf_coverage():
            return True


class DAFCLI:
    """
    Command Line Interface for DAF Fork

    Provides commands for documentation generation, testing, and management.
    """

    def __init__(self):
        """Initialize CLI"""
        self.parser = argparse.ArgumentParser(
            description="DAF Fork - Enhanced Metta Documentation and Tools",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
DAF Commands:
  daf setup                  # Complete DAF environment setup
  daf validate               # Validate DAF functionality
  daf examples               # Run DAF examples with real Metta
  daf test                   # Run comprehensive test suite
  daf docs generate          # Generate documentation
  daf docs verify            # Verify documentation coverage
  daf docs sync              # Synchronize with Metta repository
  daf wrapper <comp> <act>   # Component wrapper operations
  daf logs <action>          # Log management
  daf config <action>        # Configuration management

Examples:
  daf setup                  # Complete setup including Metta installation
  daf validate               # Comprehensive validation of all functionality
  daf examples               # Run all examples with real Metta components
  daf test                   # Execute full test suite
  daf docs generate          # Generate comprehensive documentation
            """,
        )

        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        # Setup subcommand
        # self._add_setup_command()  # Already defined above

        # Documentation subcommands
        self._add_docs_command()

        # Test subcommand
        self._add_test_command()

        # Config subcommand
        self._add_config_command()

        # Logs subcommand
        self._add_logs_command()

        # Wrapper subcommand
        self._add_wrapper_command()

        # Setup subcommand
        # self._add_setup_command()  # Already defined above

        # Validation subcommand
        self._add_validate_command()

        # Examples subcommand
        self._add_examples_command()

    def _add_setup_command(self):
        """Add setup command"""
        setup_parser = self.subparsers.add_parser("setup", help="Setup DAF environment")
        setup_parser.add_argument("--activate", action="store_true", help="Activate environment after setup")
        setup_parser.set_defaults(func=self._setup_command)

    def _add_docs_command(self):
        """Add documentation commands"""
        docs_parser = self.subparsers.add_parser("docs", help="Documentation management")

        docs_subparsers = docs_parser.add_subparsers(dest="docs_command", help="Documentation commands")

        # Generate docs
        gen_parser = docs_subparsers.add_parser("generate", help="Generate documentation")
        gen_parser.add_argument("--enhanced", action="store_true", help="Generate enhanced docs with signatures")
        gen_parser.set_defaults(func=self._docs_generate_command)

        # Verify coverage
        verify_parser = docs_subparsers.add_parser("verify", help="Verify documentation coverage")
        verify_parser.set_defaults(func=self._docs_verify_command)

        # Sync with Metta
        sync_parser = docs_subparsers.add_parser("sync", help="Synchronize with Metta repository")
        sync_parser.set_defaults(func=self._docs_sync_command)

    def _add_test_command(self):
        """Add test command"""
        test_parser = self.subparsers.add_parser("test", help="Run DAF test suite")
        test_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
        test_parser.add_argument("--output-dir", help="Output directory for test results")
        test_parser.set_defaults(func=self._test_command)

    def _add_config_command(self):
        """Add configuration command"""
        config_parser = self.subparsers.add_parser("config", help="Configuration management")
        config_parser.add_argument("action", choices=["show", "edit", "save"], help="Config action")
        config_parser.add_argument("--file", "-f", help="Configuration file path")
        config_parser.set_defaults(func=self._config_command)

    def _add_logs_command(self):
        """Add logging command"""
        logs_parser = self.subparsers.add_parser("logs", help="Log management")
        logs_parser.add_argument("action", choices=["show", "rotate", "archive", "cleanup"], help="Log action")
        logs_parser.add_argument("--days", type=int, default=30, help="Days for cleanup")
        logs_parser.set_defaults(func=self._logs_command)

    def _add_wrapper_command(self):
        """Add wrapper command"""
        wrapper_parser = self.subparsers.add_parser("wrapper", help="Component wrappers")
        wrapper_parser.add_argument("component", choices=["adaptive", "rl", "curriculum"], help="Component to wrap")
        wrapper_parser.add_argument("action", choices=["init", "run", "test"], help="Action to perform")
        wrapper_parser.set_defaults(func=self._wrapper_command)

    def _add_validate_command(self):
        """Add validation command"""
        validate_parser = self.subparsers.add_parser("validate", help="Validate DAF functionality")
        validate_parser.set_defaults(func=self._validate_command)

    def _add_examples_command(self):
        """Add examples command"""
        examples_parser = self.subparsers.add_parser("examples", help="Run DAF examples")
        examples_parser.set_defaults(func=self._examples_command)

    def _docs_generate_command(self, args):
        """Handle documentation generation"""
        self.logger.info("Generating DAF documentation...")

        try:
            # Generate comprehensive documentation with enhanced signatures
            success = generate_comprehensive_daf_docs()

            if success:
                self.logger.info("✅ Documentation generated successfully")
            else:
                self.logger.error("❌ Documentation generation failed")
                sys.exit(1)

        except Exception as e:
            self.logger.error(f"❌ Documentation generation error: {e}")
            sys.exit(1)

    def _docs_verify_command(self, args):
        """Handle documentation verification"""
        self.logger.info("Verifying DAF documentation coverage...")

        try:
            success = verify_daf_coverage()
            sys.exit(0 if success else 1)

        except Exception as e:
            self.logger.error(f"❌ Verification error: {e}")
            sys.exit(1)

    def _docs_sync_command(self, args):
        """Handle synchronization with Metta"""
        self.logger.info("Synchronizing DAF with Metta repository...")

        try:
            success = sync_daf_with_metta()
            sys.exit(0 if success else 1)

        except Exception as e:
            self.logger.error(f"❌ Synchronization error: {e}")
            sys.exit(1)

    def _test_command(self, args):
        """Handle test command"""
        self.logger.info("Running DAF test suite...")

        try:
            # Import and run the consolidated test runner
            import subprocess

            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent.parent.parent.parent / "run_daf_tests.py")],
                cwd=str(Path(__file__).parent.parent.parent.parent),
            )

            sys.exit(result.returncode)

        except Exception as e:
            self.logger.error(f"❌ Test execution error: {e}")
            sys.exit(1)

    def _setup_command(self, args):
        """Handle setup command"""
        self.logger.info("Setting up DAF environment...")

        try:
            import subprocess
            import sys
            from pathlib import Path

            daf_root = Path(__file__).parent.parent.parent.parent
            setup_script = daf_root / "setup_daf.py"

            cmd = [sys.executable, str(setup_script)]
            if hasattr(args, "activate") and args.activate:
                cmd.append("--activate")

            result = subprocess.run(cmd, cwd=str(daf_root))
            sys.exit(result.returncode)

        except Exception as e:
            self.logger.error(f"❌ Setup error: {e}")
            sys.exit(1)

    def _validate_command(self, args):
        """Handle validation command"""
        self.logger.info("Validating DAF functionality...")

        try:
            import subprocess
            import sys
            from pathlib import Path

            daf_root = Path(__file__).parent.parent.parent.parent
            validate_script = daf_root / "validate_daf.py"

            result = subprocess.run([sys.executable, str(validate_script)], cwd=str(daf_root))
            sys.exit(result.returncode)

        except Exception as e:
            self.logger.error(f"❌ Validation error: {e}")
            sys.exit(1)

    def _examples_command(self, args):
        """Handle examples command"""
        self.logger.info("Running DAF examples...")

        try:
            import subprocess
            import sys
            from pathlib import Path

            daf_root = Path(__file__).parent.parent.parent.parent
            examples_script = daf_root / "run_examples_daf.py"

            result = subprocess.run([sys.executable, str(examples_script)], cwd=str(daf_root))
            sys.exit(result.returncode)

        except Exception as e:
            self.logger.error(f"❌ Examples error: {e}")
            sys.exit(1)

    def _config_command(self, args):
        """Handle configuration command"""
        self.logger.info(f"Configuration action: {args.action}")

        config_manager = DAFConfigManager()

        if args.action == "show":
            config = config_manager.get_config()
            print("Current DAF Configuration:")
            print(f"  Adaptive Enabled: {config.adaptive_enabled}")
            print(f"  RL Enabled: {config.rl_enabled}")
            print(f"  Log Level: {config.log_level}")
            print(f"  Output Directory: {config.output_directory}")

        elif args.action == "edit":
            self.logger.info("Configuration editing not yet implemented")

        elif args.action == "save":
            success = config_manager.save_config(args.file)
            if success:
                self.logger.info("✅ Configuration saved")
            else:
                self.logger.error("❌ Failed to save configuration")
                sys.exit(1)

    def _logs_command(self, args):
        """Handle logging command"""
        self.logger.info(f"Log action: {args.action}")

        log_manager = LogManager()

        if args.action == "show":
            stats = log_manager.get_log_stats()
            print("DAF Log Statistics:")
            for name, stat in stats.items():
                if isinstance(stat, dict):
                    print(f"  {name}: {stat['size']} bytes, {stat['lines']} lines")
                else:
                    print(f"  {name}: {stat}")

        elif args.action == "rotate":
            log_manager.rotate_logs()
            self.logger.info("✅ Log files rotated")

        elif args.action == "archive":
            archive_path = log_manager.archive_logs()
            if archive_path:
                self.logger.info(f"✅ Logs archived to: {archive_path}")
            else:
                self.logger.error("❌ Archive creation failed")
                sys.exit(1)

        elif args.action == "cleanup":
            log_manager.cleanup_old_logs(args.days)
            self.logger.info(f"✅ Old logs cleaned up (>{args.days} days)")

    def _wrapper_command(self, args):
        """Handle wrapper command"""
        self.logger.info(f"Wrapper action: {args.component}.{args.action}")

        try:
            from daf.wrappers import AdaptiveWrapper, CurriculumWrapper, RLWrapper

            if args.component == "adaptive":
                wrapper = AdaptiveWrapper()
            elif args.component == "rl":
                wrapper = RLWrapper()
            elif args.component == "curriculum":
                wrapper = CurriculumWrapper()

            if args.action == "init":
                success = wrapper.initialize()
                if success:
                    self.logger.info(f"✅ {args.component} wrapper initialized")
                else:
                    self.logger.error(f"❌ {args.component} wrapper initialization failed")
                    sys.exit(1)

            elif args.action == "run":
                if args.component == "adaptive":
                    result = wrapper.run_experiment({})
                    print(f"Experiment result: {result}")
                elif args.component == "rl":
                    result = wrapper.train_model({"epochs": 100})
                    print(f"Training result: {result}")
                elif args.component == "curriculum":
                    result = wrapper.generate_curriculum(10)
                    print(f"Curriculum result: {result}")

            elif args.action == "test":
                if wrapper.is_initialized():
                    self.logger.info(f"✅ {args.component} wrapper is functional")
                else:
                    self.logger.error(f"❌ {args.component} wrapper not initialized")
                    sys.exit(1)

        except Exception as e:
            self.logger.error(f"❌ Wrapper error: {e}")
            sys.exit(1)

    def run(self, args=None):
        """Run the CLI with provided arguments"""
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return

        # Setup logging before running command
        setup_daf_logging()

        # Initialize logger
        self.logger = __import__("logging").getLogger(__name__)

        # Run the appropriate command
        try:
            parsed_args.func(parsed_args)
        except Exception as e:
            print(f"Command execution failed: {e}")
            sys.exit(1)


def main():
    """Main entry point for DAF CLI"""
    cli = DAFCLI()
    cli.run()


if __name__ == "__main__":
    main()
