import BaseHTTPServer
import os
import posixpath
import urllib
import cgi
import shutil
import mimetypes
import subprocess
import errno
import sys
from StringIO import StringIO

PORT = 8000

class BlocklyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        })

    app_serve_root_dirs = {
        '': './',
        'blockly': '../',
        }

    post_save_exec_url = 'save-and-execute'
    local_code_save_dir = './user_code/'

    def do_GET(self):
        """Serve a GET request."""
        print "GET for path " + self.path

        f = self.send_head()
        if f:
            shutil.copyfileobj(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        print "HEAD for path " + self.path

        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        path = posixpath.normpath(urllib.unquote(self.path))

        words = path.split('/')
        words = filter(None, words)

        if len(words) == 1 and words[0] == self.post_save_exec_url:
            self.do_blockly_save_exec()
        else:
            self.send_error(404, "File not found")

            
        
    def do_blockly_save_exec(self):
        length = int(self.headers['Content-Length'])
        qs = self.rfile.read(length).decode('utf-8')
        post_data = dict(cgi.parse_qsl(qs))


        if not 'fileName' in post_data or not 'code' in post_data or not post_data['fileName'] or not post_data['code']:
            self.send_error(400, 'Bad request')
            return
        
        posted_file_name = post_data['fileName']
        posted_code = post_data['code']

        try:
            os.mkdir(self.local_code_save_dir)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        target_code_file = os.path.join(self.local_code_save_dir, posted_file_name)
        save_file = open(target_code_file, 'w+')
        save_file.write(posted_code)
        save_file.close()

        try:
            exec_output = subprocess.check_output([sys.executable, target_code_file], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            exec_output = str(e) + os.linesep + e.output;
            
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(exec_output)
        self.wfile.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_serve_path(self.path)

        f = None
        if not path:
            self.send_error(404, "File not found")
            return None
        elif self.post_save_exec_url in path:
            self.send_error(405, "Method not allowed")
            return None
        elif os.path.isdir(path):
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                self.send_error(404, "File not found")
                return None

        ctype = self.guess_type(path)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            f = open(path, mode)
        except IOError:
            self.send_error(404, "File not found")
            return None

        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.end_headers()

        return f

    def translate_serve_path(self, path):
        path = posixpath.normpath(urllib.unquote(path))

        words = path.split('/')
        words = filter(None, words)

        if words and self.app_serve_root_dirs.has_key(words[0]):
            root_word = words[0]
        else:
            root_word = ''
        
        return self.app_serve_root_dirs[root_word] + path[path.index(root_word) + len(root_word):]

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        ext = ext.lower()
        
        if self.extensions_map.has_key(ext):
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']


server = BaseHTTPServer.HTTPServer(('', PORT), BlocklyRequestHandler)
print 'Server started...'
server.serve_forever()