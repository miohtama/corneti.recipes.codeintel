import os
import zc.recipe.egg


class CodeintelRecipe(object):

    def __init__(self, buildout, name, options):

        self.buildout, self.name, self.options = buildout, name, options

        # Read .codeintel directory from options or just dump in the buildout root
        default_target = os.path.join(self.buildout['buildout']['directory'], '.codeintel')
        target = options.get("codeintel-path", default_target)

        self.codeintel_directory = target

        if not os.path.exists(self.codeintel_directory):
            os.mkdir(self.codeintel_directory)

        self._python = self.buildout['buildout']['executable']

        self.extra_paths = options.get('extra-paths', '').split('\n')
        self.extra_paths = filter(lambda p: p.strip() != '', self.extra_paths)
        self.egg = zc.recipe.egg.Egg(self.buildout, self.name, self.options)

    def install(self):
        paths = self.egg.working_set()[1].entries + self.extra_paths
        paths = filter(lambda p: p.strip() != '', paths)
        open(os.path.join(self.codeintel_directory, "config"), "w").write("""\
{
    "Python": {
        "python": "%s",
        "pythonExtraPaths": [
            "%s"
        ]
    }
}
""" % (self._python, '",\n            "'.join(paths)))
        return ""

    def update(self):
        return self.install()
