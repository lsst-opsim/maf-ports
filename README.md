# maf-ports
A place to keep the tracking databases for ops2 (opsim.lsst.org) ports safe, permanent and documented.

These files are hosted on ops2.lsst.org located in Tucson, but there is a redirect from opsim.lsst.org.  The URL can be referred to as <http://opsim.lsst.org:8080> (or other port). Restricted ports can be accessed over an LSST VPN connection, or via the whitelist.

| Port | Access     | Database               | Contents |
|------|------------|------------------------|----------|
|8080  | Public     |trackingDb_curated.db   | Permanent list of all released simulated survey MAFs (e.g. Tier 1) |
|8282  | Public     |not used                |   |
|8484  | Public     |not used                |   |
|8686  | Restricted |trackingDb_verify.db    | Catalog of all MAFs from opsim4 runs (V & V)                       |
|8888  | Restricted | trackingDb_all.db      | Catalog of all MAFs from opsim3 runs                               |

Each of the tracking databases can be launched on its assigned port, assuming an installed version of sims_maf tagged with opsim4, in the following way.

```
  source /lsst_stack/loadLSST.csh
  setup sims_maf -t opsim4
  setup sims_utils -t opsim4

  cd /home
  showMaf.py -t lsst/maf-ports/trackingDb_all.db -p 8888 --noBrowser &
  showMaf.py -t lsst/maf-ports/trackingDb_verify.db -p 8686 --noBrowser &
  showMaf.py -t lsst/maf-ports/trackingDb_curated.db -p 8080 --noBrowser &
```
