#  Copyright 2014 Rackspace, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import pytest
import zvsh


class TestArgs(object):
    def test_no_args(self):
        args = zvsh.ZvArgs()
        with pytest.raises(SystemExit):
            args.parse([])

    def test_no_binary_img_args(self):
        # '--binary-image' is optional, omitting it is fine.
        cmd_line = ("zvsh --zvm-image python.tar --zvm-image myapp.tar "
                    "python myapp/main.py")
        args = zvsh.ZvArgs()
        args.parse(cmd_line.split()[1:])

    def test_correct_binary_img_arg(self):
        # '--binary-image' references one of the tar files passed via
        # '--zvm-image'
        cmd_line = ("zvsh --zvm-image python.tar --zvm-image myapp.tar "
                    "--binary-image python.tar python myapp/main.py")
        args = zvsh.ZvArgs()
        args.parse(cmd_line.split()[1:])
        assert("python.tar" == args.args.binary_image)

    def test_unknown_binary_img_arg(self):
        # '--binary-image' does *not* references any of the tar files passed
        # via '--zvm-image'
        cmd_line = ("zvsh --zvm-image python.tar --zvm-image myapp.tar "
                    "--binary-image zython.tar python myapp/main.py")
        args = zvsh.ZvArgs()
        try:
            args.parse(cmd_line.split()[1:])
        except AssertionError, e:
            expected = (
                "unknown tar file ('zython.tar') passed to '--binary-image'")
            assert expected == e.msg
        else:
            pytest.fail("AssertionError not raised")
