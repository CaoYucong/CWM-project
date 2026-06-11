# Report of Assignment 5

- Name: Yucong Cao
- Github Repo Link: [CaoYucong/CWM-Project](https://github.com/CaoYucong/CWM-project)

## Resolving URLs using DNS

### Question 1

```
ubuntu@ubuntu:~/CWM-project$ nslookup www.ox.ac.uk
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
www.ox.ac.uk	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 172.66.169.161
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 104.20.34.13

ubuntu@ubuntu:~/CWM-project$ nslookup www.baidu.com
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
www.baidu.com	canonical name = www.a.shifen.com.
www.a.shifen.com	canonical name = www.wshifen.com.
Name:	www.wshifen.com
Address: 103.235.46.102
Name:	www.wshifen.com
Address: 103.235.46.115

ubuntu@ubuntu:~/CWM-project$ nslookup www.google.com
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
Name:	www.google.com
Address: 142.251.156.119
Name:	www.google.com
Address: 142.251.152.119
Name:	www.google.com
Address: 142.251.151.119
Name:	www.google.com
Address: 142.251.153.119
Name:	www.google.com
Address: 142.251.150.119
Name:	www.google.com
Address: 142.251.155.119
Name:	www.google.com
Address: 142.251.154.119
Name:	www.google.com
Address: 142.251.157.119
Name:	www.google.com
Address: 2001:4860:482c:7700::
Name:	www.google.com
Address: 2001:4860:482a:7700::
Name:	www.google.com
Address: 2001:4860:4827:7700::
Name:	www.google.com
Address: 2001:4860:482b:7700::
Name:	www.google.com
Address: 2001:4860:4826:7700::
Name:	www.google.com
Address: 2001:4860:482d:7700::
Name:	www.google.com
Address: 2001:4860:4828:7700::
Name:	www.google.com
Address: 2001:4860:4829:7700::
```

DNS successfully translated each domain name into one or more IP addresses. Oxford and Baidu used CNAME records before reaching the final addresses, while Google returned multiple IPv4 and IPv6 addresses, demonstrating load balancing and distributed infrastructure.

### Question 2

```
ubuntu@ubuntu:~/CWM-project$ nslookup www.ox.ac.uk
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
www.ox.ac.uk	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 172.66.169.161
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 104.20.34.13
```

We are actually looking up the ip of the canonical name rather the real ox.ac.uk, which indicates that the website is protected and accelerated by Cloudflare's CDN. Two IPv4 addresses were returned, allowing traffic to be distributed across multiple servers.

### Question 3

```
ubuntu@ubuntu:~/CWM-project$ nslookup www.ox.ac.uk -norec
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
www.ox.ac.uk	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 172.66.169.161
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 104.20.34.13
```

```
ubuntu@ubuntu:~/CWM-project$ nslookup www.ox.ac.uk -norec -debug
Server:		127.0.0.53
Address:	127.0.0.53#53

------------
    QUESTIONS:
	www.ox.ac.uk, type = A, class = IN
    ANSWERS:
    ->  www.ox.ac.uk
	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
	ttl = 296
    ->  www.ox.ac.uk.cdn.cloudflare.net
	internet address = 104.20.34.13
	ttl = 48
    ->  www.ox.ac.uk.cdn.cloudflare.net
	internet address = 172.66.169.161
	ttl = 48
    AUTHORITY RECORDS:
    ADDITIONAL RECORDS:
------------
Non-authoritative answer:
www.ox.ac.uk	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 104.20.34.13
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 172.66.169.161
------------
    QUESTIONS:
	www.ox.ac.uk.cdn.cloudflare.net, type = AAAA, class = IN
    ANSWERS:
    AUTHORITY RECORDS:
    ->  cloudflare.net
	origin = ns1.cloudflare.net
	mail addr = dns.cloudflare.com
	serial = 2405009191
	refresh = 10000
	retry = 2400
	expire = 604800
	minimum = 1800
	ttl = 6
    ADDITIONAL RECORDS:
------------
```

`norec` means no recursive lookup. The result was the same as the recursive query because my local DNS resolver already had the answer cached. The `-norec` option disables recursive resolution and requests only information already known by the DNS server.

### Question 4

```
ubuntu@ubuntu:~/CWM-project$ nslookup www.ox.ac.uk 208.67.222.222
Server:		208.67.222.222
Address:	208.67.222.222#53

Non-authoritative answer:
www.ox.ac.uk	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 104.20.34.13
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 172.66.169.161

ubuntu@ubuntu:~/CWM-project$ nslookup www.ox.ac.uk 8.8.8.8
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
www.ox.ac.uk	canonical name = www.ox.ac.uk.cdn.cloudflare.net.
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 104.20.34.13
Name:	www.ox.ac.uk.cdn.cloudflare.net
Address: 172.66.169.161
```

I queried the domain using OpenDNS (208.67.222.222) and Google DNS (8.8.8.8). Both DNS providers successfully resolved the domain name and returned valid IP addresses. This demonstrates that public DNS services can independently resolve the same domain.

### Question 5

```
ubuntu@ubuntu:~/CWM-project$ nslookup 123123321uiajfhavdfgaskvwsadfr3qw.com
Server:		127.0.0.53
Address:	127.0.0.53#53

** server can't find 123123321uiajfhavdfgaskvwsadfr3qw.com: NXDOMAIN
```

When I attempted to resolve a non-existent domain, the DNS server returned an `NXDOMAIN` response. This indicates that the requested domain name does not exist in the DNS and therefore cannot be resolved to an IP address.

### Question 6

```
ubuntu@ubuntu:~/CWM-project$ nslookup 104.20.34.13
** server can't find 13.34.20.104.in-addr.arpa: NXDOMAIN

ubuntu@ubuntu:~/CWM-project$ nslookup 8.8.8.8
8.8.8.8.in-addr.arpa	name = dns.google.
```

Some addresses successfully returned hostnames because PTR records were configured. Other addresses did not return results because no reverse DNS records were available.

## DYN DNS Failure

### Question 1

The DNS servers are spread around the globe.

### Question 2

Too many request used up all the resources of the DNS server, where most of the request are made just to attack the servers, so that normal users would be difficult to have respond from the server. This is a distributed denial of service attack.

### Question 3

A lot of companies are affected. For instance, amazon or github, those company who use the Dyn DNS server would be not accessible since normal user can't get the IP address of those companys' website.

### Question 4

Europe and North America, especially the Eastern United States

### Question 5

The only public threat that's been made was a single tweet (account since deleted) threatening both media and government outlets for "spreading false propaganda."

### Question 6

- Filter out the attack stream.
- Expand capacity

### Question 7

- Companies and governments shouldn't rely on single solution of DNS server/ Instead, they should use multiple DNS service to limit the effect of one of the server being down.
- Use redundant backups for server resources to improve resilience.
- Spread the server so they are not on the same address.

- Companies should not rely on a single DNS provider. A better defense is to use multiple DNS providers or secondary DNS, add failover and redundancy, and strengthen DDoS filtering, rate limiting, and monitoring. 

## DNS Failure Case Study

## Cloudflare 1.1.1.1 DNS Outage (July 14, 2025)

### Background

Cloudflare provides the public DNS resolver service `1.1.1.1` , which is one of the most widely used DNS services in the world. Many users and companies rely on it to resolve domain names into IP addresses. On July 14, 2025, Cloudflare experienced a major DNS outage that affected users globally. 

The outage started at 21:52 UTC and lasted for approximately 62 minutes. During this period, users who were using Cloudflare's 1.1.1.1 resolver could not resolve domain names, making many websites and online services inaccessible. The majority of Cloudflare DNS users around the world were affected. 

### Cause of the Failure

The problem originated from a configuration change made on June 6, 2025. During that update, the IP prefixes used by the 1.1.1.1 DNS service were accidentally associated with a non-production service. The error remained hidden for over a month. On July 14, another routine configuration update triggered a global refresh of network settings, causing the DNS routes for 1.1.1.1 to be withdrawn worldwide. As a result, users could no longer reach the DNS servers. 

### Recovery

Cloudflare detected the issue shortly after it began and declared an incident. Engineers reverted the faulty configuration and restored the DNS route advertisements. Full service was restored at 22:54 UTC, ending the outage. 

### Conclusion

This incident shows how a small configuration mistake can have a large impact on Internet users worldwide. Even though no cyber attack occurred, the outage demonstrated the importance of redundancy, careful change management, and reliable monitoring for critical DNS services. 