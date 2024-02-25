import http.server as hs
import sys
import json
import cgi
import urllib.parse


class ServerHTTPHandler(hs.BaseHTTPRequestHandler):
    def respond_with_json(self, json_object):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(json_object).encode("utf-8"))

    def respond_with_image(self, image_object):
        self.send_response(200)
        self.send_header('Content-Type', 'image/png')
        self.end_headers()
        self.wfile.write(image_object)

    def check_getmany_path(self):
        path_array = self.path.split('/')[1:]
        return len(path_array) == 1 and path_array[0] == 'products'

    def check_post_path(self):
        path_array = self.path.split('/')[1:]
        return len(path_array) == 1 and path_array[0] == 'product'

    def check_get_path(self):
        path_array = self.path.split('/')[1:]
        if not (len(path_array) == 2 and path_array[0] == 'product' and path_array[1].isdigit()):
            return 0
        return int(path_array[1])

    def check_image_path(self):
        path_array = self.path.split('/')[1:]
        if not (len(path_array) == 3 and path_array[0] == 'product' and \
           path_array[1].isdigit() and \
           path_array[2] == 'image'):
            return 0
        return int(path_array[1])

    def parse_json_body(self):
        content_len = int(self.headers.get('Content-Length'))
        json_body = self.rfile.read(content_len)

        try:
            return json.loads(json_body)
        except:
            return None

    def do_GET(self):
        # check if requested to list all products

        if self.check_getmany_path():
            product_array = []
            for _, v in product_dict.items():
                product_array.append(v)
            self.respond_with_json(product_array)
            return

        # check if requested to get image

        product_id = self.check_image_path()
        if product_id:
            
            if product_id not in product_images:
                self.send_error(404)
                return

            image = product_images[product_id]
            self.respond_with_image(image)
            return

        # default get query: get product by id

        product_id = self.check_get_path()
        if product_id not in product_dict:
            self.send_error(404)
            return

        product = product_dict[product_id]
        self.respond_with_json(product)

    def do_POST(self):
        global product_count

        # check if requested to post image

        product_id = self.check_image_path()
        if product_id:

            if product_id not in product_dict:
                self.send_error(404)
                return

            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            image = cgi.parse_multipart(self.rfile, pdict)['icon'][0]

            product_images[product_id] = image
            self.send_response(200)
            self.end_headers()
            return

        # default post query: add product
            
        if not self.check_post_path():
            self.send_error(404)
            return

        product = self.parse_json_body()

        if not product:
            self.send_error(404)
            return

        product_count += 1
        product['id'] = product_count
        product_dict[product_count] = product
        self.respond_with_json(product)

    def do_PUT(self):
        product_id = self.check_get_path()
        if product_id not in product_dict.keys():
            self.send_error(404)
            return

        new_product = self.parse_json_body()

        if not new_product:
            self.send_error(404)
            return

        for key in new_product.keys():
            if key == 'id':
                continue
            product_dict[product_id][key] = new_product[key]
            
        self.respond_with_json(product_dict[product_id])

    def do_DELETE(self):
        product_id = self.check_get_path()

        if product_id not in product_dict.keys():
            self.send_error(404)
            return

        product = product_dict[product_id]
        product_dict.pop(product_id)

        if product_id in product_images:
            product_images.pop(product_id)

        self.respond_with_json(product)


def run(argv):
    global product_dict, product_count
    server = hs.HTTPServer(('127.0.0.1', 7777), ServerHTTPHandler)
    server.serve_forever()


if __name__ == '__main__':
    product_dict = {}
    product_images = {}
    product_count = 0
    run(sys.argv)
