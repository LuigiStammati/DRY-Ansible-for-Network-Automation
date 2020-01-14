#!/usr/bin/python


# --------------------------------------
# Filters
# --------------------------------------

class FilterModule(object):

    def filters(self):
        return {
            'filter_bundle_groups': self.filter_bundle_groups,
        }

    def filter_bundle_groups(self, groups, start_with="lag_bundle"):
        """
        Filter the groups whose names start with the provided start_with parameter. Default is 'lag_bundle'
        :param groups:
        :param start_with:
        :return:
        """
        return [g for g in groups if g.startswith(start_with)]

