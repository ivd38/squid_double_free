SQUID 5.6 double free


Double free issue in NTLM SMB_LM authenticator.

```
int
RFCNB_Recv(void *con_Handle, struct RFCNB_Pkt *Data, int Length)
{
...
      pkt = RFCNB_Alloc_Pkt(RFCNB_Pkt_Hdr_Len);

    if (pkt == NULL) {

        RFCNB_errno = RFCNBE_NoSpace;
        RFCNB_saved_errno = errno;
        return (RFCNBE_Bad);

    }
[1]    pkt->next = Data;           /* Plug in the data portion */

    if ((ret_len = RFCNB_Get_Pkt(con_Handle, pkt, Length + RFCNB_Pkt_Hdr_Len)) < 0) {
[2]        RFCNB_Free_Pkt(pkt);
        return (RFCNBE_Bad);

    }
    /* We should check that we go a message and not a keep alive */

    pkt->next = NULL;

    RFCNB_Free_Pkt(pkt);
}
```

Note that pkt->next is a ptr to Data.
In case of error it will be freed on line #2.
Free_Pkt also calls free on pkt->next.
When 'Data' is freed again double free happens.

How to reproduce:
```
1. build squid
$  ./configure --prefix=/var/squid --enable-auth-ntlm=SMB_LM && make

2. run smb server
# ./s1.py

3. run authenticator
$ echo "YR" | ./ntlm_smb_lm_auth localhost/localhost
```


Asan log attached.
