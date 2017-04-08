# maf-ports
A place to keep the tracking databases for ops2 (opsim.lsst.org) ports safe, permanent and documented.

These files are hosted on ops2.lsst.org located in Tucson, but there is a redirect from opsim.lsst.org.  The URL can be referred to as <http://opsim.lsst.org:8080> (or other port).

```
  source /lsst_stack/loadLSST.csh
  setup sims_maf -t opsim4
  setup sims_utils -t opsim4

  cd /home
  showMaf.py -t lsst/maf-ports/trackingDb_all.db -p 8888 --noBrowser &
  showMaf.py -t lsst/maf-ports/trackingDb_verify.db -p 8686 --noBrowser &
  showMaf.py -t lsst/maf-ports/trackingDb_curated.db -p 8080 --noBrowser &
```
