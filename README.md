# Selenium Informer  

---

> This tool has been developed by Marcos Carro [@30vh1_](https://twitter.com/30vh1_), more information can be found [here][Tarlogic Post URL].

## About

Selenium informer is a tool developed as a *Proof of Concept* for analyzing [Selenium Grid][Selenium Grid URL] environments.  

It's main purpose is to, given the location of a Selenium Hub console, list all nodes subscribed do it and check which are vulnerable to Remote Code Execution.  For doing this, the  online service ```dns.requestbin.net``` is used in order to exfiltrate information through DNS.

## seleniumInformer.py  

Selenium informer accepts as command line parameters three options, the hub IP address, the port the hub is listening on and as an optional trigger, the tool allows just for enumerating the nodes subscribed to the hub.

```shell
./seleniumInformer.py -h
usage: seleniumInformer.py [-h] [-a ADDR] [-p PORT] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDR, --addr ADDR  Hub ip address
  -p PORT, --port PORT  Hub web panel port
  -e, --enumerate       Just eumerate nodes on hub
```

### Enumerating nodes on hub

* For enumerating nodes on a hub the **-e, --enumerate** trigger must be used.

![](https://github.com/TarlogicSecurity/seleniumInformer/blob/master/exec_result_just_enumerate.png?raw=true)

* By default the tool checks which of the nodes subscribed to a hub are vulnerable to RCE (without the **-e, --enumerate** trigger)  

![](https://github.com/TarlogicSecurity/seleniumInformer/blob/master/exec_result.png?raw=true)

---

[Selenium Grid URL]: https://www.seleniumhq.org/docs/07_selenium_grid.jsp
[Tarlogic Post URL]:  https://www.tarlogic.com/en/blog/attacking-selenium-grid/
