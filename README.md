XPD-Psych-DS
=============

Create data set that is compliant to the *Psychology Data Standard* 
([Psych-DS](https://github.com/psych-ds/psych-DS)) from an existing 
[Expyriment](http://www.expyriment.org) data set.

---

*Released under the GNU General Public License v3* 

Oliver Lindemann (oliver@expyriment.org)



Install
-------

```
python3 -m pip install --index-url https://test.pypi.org/simple/ xpd-psych-ds
```


Command line tool
------------------

```
python3 -m xpd_to_psych_ds.cli -h
```

or if installed correctly:

```
xpd_to_psych_ds -h
```

Python example
--------------

```
import xpd_psych_ds
xpd_psych_ds.create(data_folder="expyriment_data", 
                    additional_data_folder=["events"],
                    override_existing_folder=True)
```
