import csv
import concurrent.futures


# read csv and return a list of dicts
def read_csv_to_dict(input_filename: str) -> list:
    with open(input_filename) as csvfile:
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)
        if has_header:
            reader = csv.DictReader(csvfile)
        else:
            field_names = [
                "source_id",
                "url",
                "nr_a",
                "nr_b",
                "nr_c",
                "clef",
                "keysig",
                "timesig",
                "notes"]
            reader = csv.DictReader(csvfile, fieldnames=field_names)

        # for testing: reduce number of incipits to be checked
        return list(reader)[:100000]


# pack clef, keysig, timesig and notes to a single string and add incipit key
def pack_incipits(list_of_incipits: list) -> None:
    for inc in list_of_incipits:
        incipit_temp = ''
        if inc['clef']:
            incipit_temp = incipit_temp + '%' + inc.get('clef')
        if inc['keysig']:
            incipit_temp = incipit_temp + '$' + inc.get('keysig')
        if inc['timesig']:
            incipit_temp = incipit_temp + '@' + inc.get('timesig')
        if inc['notes']:
            incipit_temp = incipit_temp + ' ' + inc.get('notes')
        inc.update({'incipit': incipit_temp})


def check_incipit(incipit_to_check: dict) -> dict:
    parse_results: dict = parse_incipit(incipit_to_check.get('incipit'))
    is_valid: bool = parse_results.get("valid")
    num_errors: int = parse_results.get("num_errors")
    syntax_errors: list = parse_results.get("syntax_errors")

    if not is_valid:
        result = {'num_errors': num_errors,
                  #'segment':[serr.get("location") for serr in syntax_errors[-num_errors:]],
                  #'message':[serr.get("msg") for serr in syntax_errors[-num_errors:]]})
                  'segment': [serr.get("location") for serr in syntax_errors],
                  'message': [serr.get("msg") for serr in syntax_errors]}
    else:
        result = {'num_errors': num_errors,
                  'segment': [],
                  'message': []}
    # test (maybe not necessary): clear syntax_errors to avoid potential problems
    # of different cores appending and reading the same list
    syntax_errors.clear()

    return result


def run_check(list_of_incipits: list, parallel_computation: bool) -> None:
    if parallel_computation:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for res, inc in zip(executor.map(
                    check_incipit, list_of_incipits), list_of_incipits):
                inc.update(res)
    else:
        for inc in list_of_incipits:
            inc.update(check_incipit(inc))


def write_to_csv(list_of_incipits: list, output: str) -> None:
    with open(output, "w") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=[
                *list_of_incipits[0].keys()])
        writer.writeheader()
        for inc in list_of_incipits:
            inc_temp = inc.copy()
            num_errors = inc.get('num_errors')
            for j in range(num_errors):
                inc_temp['segment'] = inc.get('segment')[j]
                inc_temp['message'] = inc.get('message')[j]
                writer.writerow(inc_temp)


if __name__ == "__main__":
    import sys
    sys.path.append('../pypaec')
    from pypaec import parse_incipit

    list_of_incipits = read_csv_to_dict(sys.argv[1])
    pack_incipits(list_of_incipits)
    run_check(list_of_incipits, False)
    write_to_csv(list_of_incipits, "incipit_report_test_ser2.csv")

    num_incipits = len(list_of_incipits)
    num_incipits_to_check = len(
        [inc.get('num_errors') for inc in list_of_incipits if inc.get('num_errors') > 0])

    print(f"Number of incipits checked: {num_incipits}")
    print(f"Number of incipits to check: {num_incipits_to_check}")
    print(f"Error rate: {(num_incipits_to_check / num_incipits) * 100}%")
