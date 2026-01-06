import pathlib
import sys
import typing

from .validation import AuditorLevel, get_cohort_auditor, get_phenopacket_auditor
from .io import read_phenopacket, read_cohort, read_phenopackets


try:
    import click
except ImportError:
    print("Click is required for the CLI. Please install it via 'pip install phenosentry[cli]'")
    exit(1)


@click.group()
def main():
    pass


@main.command("validate")
@click.option("--path", type=click.Path(exists=True, readable=True), required=True)
@click.option(
    "--level",
    type=click.Choice([m.value for m in AuditorLevel]),
    default="default",
    help="The level of validation to perform: strict or default.",
)
@click.option("--is-cohort", is_flag=True, help="Indicates that the input is a cohort.")
def validate(
    path,
    level: typing.Literal["default", "strict"],  # type: ignore
    is_cohort: bool = False,
):
    """
    Validates phenopacket or cohort data based on the provided options.

    Args:
        path (str): The file or directory path to the phenopacket(s) or cohort.
        level (str): The validation level, either 'strict' or 'default'.
        is_cohort (bool): Flag indicating whether the input is a cohort.

    Returns:
        int: 0 if validation passes without errors or warnings, 1 otherwise.
    """
    pathed = pathlib.Path(path)
    level: AuditorLevel = AuditorLevel[level.upper()]
    if pathed.is_file():
        phenopacket = read_phenopacket(
            path=pathed,
        )
        # single phenopacket
        auditor = get_phenopacket_auditor(level)
        notepad = auditor.prepare_notepad(auditor.id())
        auditor.audit(
            item=phenopacket,
            notepad=notepad,
        )
    elif pathed.is_dir():
        # cohort of phenopackets
        if is_cohort:
            cohort = read_cohort(directory=pathed)
            auditor = get_cohort_auditor()
            notepad = auditor.prepare_notepad(auditor.id())
            auditor.audit(
                item=cohort,
                notepad=notepad,
            )
        else:
            # We iterate phenopackets and validate them seperately
            auditor = get_phenopacket_auditor(level)
            notepad = auditor.prepare_notepad(auditor.id())
            phenopackets = read_phenopackets(pathed)
            for phenopacket in phenopackets:
                notepad.add_subsection("Phenopacket {}".format(phenopacket.id))
                auditor.audit(
                    item=phenopacket,
                    notepad=notepad,
                )
    else:
        # TODO: troubleshoot
        print("Invalid CLI configuration", file=sys.stderr)
        return 1

    # TODO: Notepad summary should include source data and spot of issue
    if notepad.has_errors_or_warnings(include_subsections=True):
        notepad.summarize(file=sys.stderr)  # type: ignore
        return 1
    else:
        notepad.summarize(file=sys.stderr)  # type: ignore
        return 0


if __name__ == "__main__":
    main()
