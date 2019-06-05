import logging

from flask_restplus import Api, Swagger
from werkzeug import cached_property

logger = logging.getLogger('api')


def attach_dict(dest, source):
    """
    copy source structure data to dest and store
    :param dest: destination object dict|list
    :param source: source object dict|list
    :return:
    """
    if isinstance(dest, dict):
        if isinstance(source, dict):
            for item, value in source.items():
                if item in dest:
                    if isinstance(dest[item], dict) or isinstance(dest[item], list):
                        attach_dict(dest[item], value)
                    else:
                        dest[item] = value
                else:
                    dest[item] = value
    elif isinstance(dest, list):
        if isinstance(source, list):
            dest += source
        else:
            dest.append(source)


class CustomSwagger(Swagger):
    """Override RESTplus Swagger class to add custom properties."""

    def as_dict(self, custom_definition):
        """Add custom properties to top-level Swagger specs."""
        specs = super().as_dict()
        # specs['x-api-definition'] = 'custom value'
        attach_dict(specs, custom_definition)
        return specs


class CustomApi(Api):
    """
    Override Swagger API
    """
    _custom_definition = {}

    @cached_property
    def __schema__(self):
        """
        The Swagger specifications/schema for this API

        Override this to refer to our fixed Swagger class.

        :returns dict: the schema as a serializable dict
        """
        if not self._schema:
            try:
                self._schema = CustomSwagger(self).as_dict(self._custom_definition)
            except Exception:
                # Log the source exception for debugging purpose
                # and return an error message
                msg = 'Unable to render schema'
                logger.exception(msg)  # This will provide a full traceback
                return {'error': msg}
        return self._schema

    def _add_xtag_group(self, tag_group_name, tag):
        """
        insert xtag_group into API
        :param tag_group_name: Name of a Group
        :param tag: Namespace 's name
        :return:
        """
        # add x tags property if not exists
        if 'x-tagGroups' not in self._custom_definition:
            self._custom_definition['x-tagGroups'] = []
        tmp_dict = None
        for item in self._custom_definition['x-tagGroups']:
            if tag_group_name == item['name']:
                tmp_dict = item
                break

        if tmp_dict:
            tmp_dict['tags'].append(tag)
        else:
            self._custom_definition['x-tagGroups'].append(
                {
                    'name': tag_group_name,
                    'tags': [tag]
                }
            )


    def add_namespace(self, ns, path=None, tag_group_name=None):
        """
        This method override parent class to add function for xtags_group
        :param Namespace ns: the namespace
        :param path: registration prefix of namespace
        :param tag_group_name: add this namespace to group
        :return:
        """
        super().add_namespace(ns, path)
        if tag_group_name:
            # self.add_custom_definition({
            #     'x-tagGroups': [
            #         {
            #             'name': x_tag_group,
            #             'tags': [ns.name]
            #         }
            #     ]
            # })
            self._add_xtag_group(tag_group_name, ns.name)

    def add_custom_definition(self, source_dict):
        """
        Add custom definition dict to obj for storing
        :param source_dict:
        :return:
        """
        attach_dict(self._custom_definition, source_dict)
