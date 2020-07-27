#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import yaml
import argparse
from datadog import initialize, api
from operator import itemgetter


def arg_parse(bin_dir):
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-f', '--filter', type=str,
                        help='query to filter search results', default="")
    parser.add_argument('-c', '--conf-yaml', type=str,
                        help='define yaml specify the metadata', default=f"{bin_dir}/include_keys.yml")
    parser.add_argument('-a', '--add', action='store_true',
                        help='add/update user tag')
    return(parser.parse_args())


def select_metadata(include_keys, metadata):
    result = []
    for include_key in include_keys.keys():
        if include_key in metadata:
            include_key_type = type(include_keys[include_key])
            if include_key_type is dict:
                user_tags = select_metadata(
                    include_keys[include_key], metadata[include_key])
                result.extend(user_tags)
            elif include_key_type is list:
                print(f"\"{include_key}\" list type not supported")
            else:
                user_tag = f"{include_keys[include_key]}:{metadata[include_key]}"
                result.append(user_tag)
    return result


def main():
    bin_dir = os.path.dirname(os.path.abspath(__file__))

    args = arg_parse(bin_dir)
    if 'DD_API_KEY' not in os.environ or 'DD_APP_KEY' not in os.environ:
        return "API key is not set."

    add_metadata(args.filter, args.conf_yaml, args.add)


def add_metadata(filter="", conf_yaml="./include_keys.yml", add=False):
    with open(conf_yaml, 'r') as yml:
        include_keys = yaml.safe_load(yml)

    initialize()
    res = api.Hosts.search(filter=filter)

    host_list = []
    for host in res['host_list']:
        host['user_tag_count'] = 0
        if 'tags_by_source' in host:
            if 'Users' in host['tags_by_source']:
                host['user_tag_count'] = len(host['tags_by_source']['Users'])
        host_list.append(host)
    host_list.sort(key=itemgetter('user_tag_count'))

    for host in host_list:
        # name == Datadog's host
        datadogs_host = host['name']
        print(f"# host: {datadogs_host}")

        metadata = select_metadata(include_keys, host)
        print(f"metadata: {metadata}")

        before_tags = host['tags_by_source']['Users'] if host['user_tag_count'] > 0 else [
        ]
        before_tags.sort()
        print(f"before: {before_tags}")

        update_tags = metadata
        for before_tag in before_tags:
            preserve = True
            if ":" in before_tag:
                before_tag_key = before_tag.split(':')[0] + ":"
            else:
                before_tag_key = before_tag
            for update_tag in update_tags:
                if update_tag.startswith(before_tag_key):
                    preserve = False
            if preserve:
                update_tags.append(before_tag)
        update_tags.sort()

        if before_tags == update_tags:
            print("skipped")
        else:
            if add:
                try:
                    res = api.Tag.update(
                        datadogs_host, tags=update_tags, source="Users")
                    print(f"updated: {res}")
                except Exception as e:
                    raise e
            else:
                print(f"[dryrun] update_tags: {update_tags}")


if __name__ == '__main__':
    main()
