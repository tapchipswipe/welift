# The Inlets pilot week — checklist

Run after Access Desk + (ideally) real gate codes work. Soft pilot = CAM written OK.

## Cast

- [ ] CAM contact confirmed  
- [ ] 1 SMB vendor (owner phone — Access Desk send)  
- [ ] 1 multi-crew vendor (dispatch forwards or portal later)  

## Week script

| Day | Activity | Done |
|-----|----------|------|
| Mon | CAM adds/confirms vendors on Access Desk; send test code | [ ] |
| Tue | Standing vendor keypad entry with SMS code | [ ] |
| Wed | AI forgot-code path with proof PIN | [ ] |
| Thu | Revoke drill + wrong-PIN deny | [ ] |
| Fri | Review audit with CAM; ask to continue | [ ] |

## Success metrics

- [ ] ≥3 keypad (or simulated) verified entries  
- [ ] AI calls ≤ keypad entries for standing vendors  
- [ ] Zero wrong-admits  
- [ ] CAM verbal interest to continue  

## Logs

- `data/credentials.json` deliveries  
- `data/events.jsonl` / serverless logs  
- Retell call recordings  

Related: [PRODUCT.md](PRODUCT.md) · [SALES-DEMO.md](SALES-DEMO.md) · [GATE-CODE-RUNBOOK.md](GATE-CODE-RUNBOOK.md)
