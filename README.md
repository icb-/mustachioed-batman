## Example Juniper config
    protocols {
        bgp {
            group RTBH {
                type external;
                description RTBH;
                import RTBH-IN;
                export DENY-ALL;
                peer-as 65501;
                local-as 65500;
                neighbor 192.168.2.66;
            }
        }
    }
    policy-options {
        policy-statement RTBH-IN {
            term RTBH-IN {
                from protocol bgp;
                then {
                    community add DONT-ANNOUNCE;
                    next-hop discard;
                    accept;
                }
            }
            then reject;
        }
        policy-statement DENY-ALL {
            then reject;
        }
        community DONT-ANNOUNCE members 65500:666;
    }
