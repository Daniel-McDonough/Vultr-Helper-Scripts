# Vultr Helper Scripts

#### Some scripts to make working with Vultr less tedious.


---

### vultr-instance.py


Lists instances with details and import them into Terraform.
```
usage: vultr-instance.py [-h] [-i] [-v]

Vultr Instance Helper.

options:
  -h, --help     show this help message and exit
  -i, --imports  Import an instance
  -v, --verbose  Print instance details

Reads API key from VULTR_API_KEY envar.
```

Verbose Output:
```
Instances in your Vultr account:
1. daniel-mcdonough.com
- Name: daniel-mcdonough.com
  ID: 2f0191f8-7746-444a-91a1-e81939171bd9
  Status: active
  IP: xxx.xxx.xxx.xxx
  Plan: vc2-1c-1gb
  Region: atl
```

### Limitations

No pagination support at the moment. This will only be an issue with > 200 instances.
