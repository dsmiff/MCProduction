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

## Convert LHE to EDM LHE ROOT File

To convert a `.lhe` file into a CMS EDM ROOT file.

Create a temporary directory with your LHEs:
```
python mc-production/scripts/CopyToTemp.py -i <lhe dir> -o _tmp
```
Then run `cmsDriver.py` on an LHE file to create a config:
```
cmsDriver.py MCDBtoEDM --conditions MCRUN2_71_V1::All -s NONE --eventcontent RAWSIM --datatier GEN --filein file:_tmp/<file>.lhe --no_exec
```
To produce the ROOT file, run `cmsRun MCDBtoEDM_NONE.py`.