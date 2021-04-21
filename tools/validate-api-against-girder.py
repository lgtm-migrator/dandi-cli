#!/usr/bin/env python3
import click
import requests

from dandi.dandiapi import DandiAPIClient
from dandi.dandiset import APIDandiset
from dandi.girder import GirderCli


@click.command()
def main():
    g_client = GirderCli("http://3.19.164.171")
    a_client = DandiAPIClient("https://api.dandiarchive.org/api")

    with a_client.session():
        g_client.dandi_authenticate()
        # gather all dandisets known to girder: hardcoded _id for "drafts" collection
        g_dandisets = list(
            g_client.listFolder("5e59bb0af19e820ab6ea6c62", "collection")
        )
        for dandiset, girder_id in [(x["name"], x["_id"]) for x in g_dandisets]:
            print(f"DANDI:{dandiset}", end="\t")
            g_meta, g_assets_ = g_client.get_dandiset_and_assets(girder_id, "folder")
            g_assets = list(g_assets_)
            # harmonize and get only what we care about ATM - path and size,
            # or otherwise we would need to query each asset for metadata
            g_assets_h = set((a["path"].lstrip("/"), a["size"]) for a in g_assets)

            a_meta, a_assets_ = a_client.get_dandiset_and_assets(dandiset, "draft")
            a_assets = list(a_assets_)
            a_assets_h = set((a["path"].lstrip("/"), a["size"]) for a in a_assets)

            if a_assets_h != g_assets_h:
                print("differs")
                import pdb

                pdb.set_trace()
            else:
                print(f"{len(a_assets)} assets the same")


if __name__ == "__main__":
    main()
