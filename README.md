# ProdDMS
Production of DMS Monte Carlos samples

[https://twiki.cern.ch/twiki/bin/viewauth/CMS/DMRA1](https://twiki.cern.ch/twiki/bin/viewauth/CMS/DMRA1)

# Private production

For private production of MC Samples and Detector Simulation

## Uncompressing LHEs

If LHE files are in a `event.lhe.gz` format, you can uncompress them with:

```
python mc-production/scripts/UncompressLHE.py -i <directory to lhes>
```

## Merging LHEs

To merge LHE files (taken from CMSSW):

```
cd mc-production/scripts
g++ -Wall -o mergeLheFiles mergeLheFiles.cpp
ls _tmpdir/*.lhe > lheList
./mergeLheFiles lheList
```