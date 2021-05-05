import json
import re
import base64
import argparse
import sys
from attacknav_template import TEMPLATE_B64


def extract_techniques(input_file):
    input_file = open(input_file)
    p = re.compile("T\d\d\d\d")
    matches = p.findall(input_file.read())
    return matches


def get_template(filename):
    if filename == "default":
        template_dict = json.loads(base64.b64decode(TEMPLATE_B64).decode("ascii"))
    else:
        template = open(filename)
        template_dict = json.load(template)
    return template_dict


def write_template(template_dict, filename=""):
    outfile = open(filename, "w")
    outfile.write(json.dumps(template_dict))
    outfile.close()
    print("Wrote ATT&CK navigator layer to " + filename)


def align_ttps(template_dict, techniques, score=5):
    for techniques in techniques:
        for item in template_dict["techniques"]:
            if techniques == item["techniqueID"]:
                item.update({"score": score})


def set_actor(actor_name, template):
    template.update({"name": actor_name + " TTPs"})


def main():
    """Console script for techid_to_attack_nav."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_file",
        help="Specify the input file that contains technique IDs",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Specify the actor or tool name for the title of the resulting layer",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--template_file",
        help="Specify the ATT&CK Navigator layer .JSON template you would like to use",
        default="default",
    )
    parser.add_argument(
        "-s",
        "--score",
        help="Specify the score for the techniques (defaults to 5)",
        default=5,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="Specify the file for the resulting template layer .JSON content",
        default="results.json",
    )
    args = parser.parse_args()

    techniques = extract_techniques(args.input_file)
    template = get_template(args.template_file)
    set_actor(args.name, template)
    align_ttps(template, techniques, args.score)
    write_template(template, args.output_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
