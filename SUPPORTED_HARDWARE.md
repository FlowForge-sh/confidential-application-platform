## AMD
Generally 7003 and above is a good choice.

Encrypted State (ES) – formerly known as SEV-ESSEV-ES encrypts all CPU register contents when a VM stops running. This prevents the leakage of information in CPU registers to components like the hypervisor and can even detect malicious modifications to a CPU register state.

**7003 and above:**
**Secure Nested Paging (SNP)** – formerly known as SEV-SNPSEV-SNP adds strong memory integrity protection to help prevent malicious hypervisor-based attacks like data replay, memory re-mapping, and more to create an isolated execution environment. Also, SEV-SNP introduces several additional optional security enhancements designed to support additional VM use models, offer stronger protection around interrupt behavior, and offer increased protection against recently disclosed side channel attacks.
https://www.amd.com/en/developer/sev.html
<img width="1434" height="486" alt="image" src="https://github.com/user-attachments/assets/865c37e5-2d21-4033-94f4-79f5ed5f83f2" />


## Intel TDX
### List of processors that support Intel TDX
```
Intel® Xeon® 6756P-B Processor
Intel® Xeon® 6766P-B Processor
Intel® Xeon® 6768P-B Processor
Intel® Xeon® 6776P-B Processor
Intel® Xeon® 6518P-B Processor
Intel® Xeon® 6544P-B Processor
Intel® Xeon® 6548P-B Processor
Intel® Xeon® 6718P-B Processor
Intel® Xeon® 6725P Processor
Intel® Xeon® 6532P-B Processor
Intel® Xeon® 6962P Processor
Intel® Xeon® 6978P Processor
Intel® Xeon® 6732P Processor
Intel® Xeon® 6774P Processor
Intel® Xeon® 6776P Processor
Intel® Xeon® 6716P-B Processor
Intel® Xeon® 6745P Processor
Intel® Xeon® 6315P Processor
Intel® Xeon® 6325P Processor
Intel® Xeon® 6333P Processor
Intel® Xeon® 6337P Processor
Intel® Xeon® 6349P Processor
Intel® Xeon® 6353P Processor
Intel® Xeon® 6357P Processor
Intel® Xeon® 6369P Processor
Intel® Xeon® 6503P-B Processor
Intel® Xeon® 6505P Processor
Intel® Xeon® 6507P Processor
Intel® Xeon® 6511P Processor
Intel® Xeon® 6513P-B Processor
Intel® Xeon® 6515P Processor
Intel® Xeon® 6516P-B Processor
Intel® Xeon® 6517P Processor
Intel® Xeon® 6520P Processor
Intel® Xeon® 6521P Processor
Intel® Xeon® 6523P-B Processor
Intel® Xeon® 6527P Processor
Intel® Xeon® 6530P Processor
Intel® Xeon® 6533P-B Processor
Intel® Xeon® 6543P-B Processor
Intel® Xeon® 6546P-B Processor
Intel® Xeon® 6553P-B Processor
Intel® Xeon® 6556P-B Processor
Intel® Xeon® 6563P-B Processor
Intel® Xeon® 6706P-B Processor
Intel® Xeon® 6714P Processor
Intel® Xeon® 6724P Processor
Intel® Xeon® 6726P-B Processor
Intel® Xeon® 6728P Processor
Intel® Xeon® 6730P Processor
Intel® Xeon® 6731P Processor
Intel® Xeon® 6736P Processor
Intel® Xeon® 6737P Processor
Intel® Xeon® 6738P Processor
Intel® Xeon® 6740P Processor
Intel® Xeon® 6741P Processor
Intel® Xeon® 6747P Processor
Intel® Xeon® 6748P Processor
Intel® Xeon® 6760P Processor
Intel® Xeon® 6761P Processor
Intel® Xeon® 6767P Processor
Intel® Xeon® 6768P Processor
Intel® Xeon® 6781P Processor
Intel® Xeon® 6787P Processor
Intel® Xeon® 6788P Processor
Intel® Xeon® 6944P Processor
Intel® Xeon® 6952P Processor
Intel® Xeon® 6960P Processor
Intel® Xeon® 6972P Processor
Intel® Xeon® 6979P Processor
Intel® Xeon® 6980P Processor
Intel® Xeon® 6710E Processor
Intel® Xeon® 6731E Processor
Intel® Xeon® 6740E Processor
Intel® Xeon® 6746E Processor
Intel® Xeon® 6756E Processor
Intel® Xeon® 6766E Processor
Intel® Xeon® 6780E Processor
Intel® Xeon® Bronze 3508U Processor
Intel® Xeon® Gold 5512U Processor
Intel® Xeon® Gold 5515+ Processor
Intel® Xeon® Gold 5520+ Processor
Intel® Xeon® Gold 6526Y Processor
Intel® Xeon® Gold 6530 Processor
Intel® Xeon® Gold 6534 Processor
Intel® Xeon® Gold 6538N Processor
Intel® Xeon® Gold 6538Y+ Processor
Intel® Xeon® Gold 6542Y Processor
Intel® Xeon® Gold 6544Y Processor
Intel® Xeon® Gold 6548N Processor
Intel® Xeon® Gold 6548Y+ Processor
Intel® Xeon® Gold 6554S Processor
Intel® Xeon® Gold 6558Q Processor
Intel® Xeon® Platinum 8558 Processor
Intel® Xeon® Platinum 8558P Processor
Intel® Xeon® Platinum 8558U Processor
Intel® Xeon® Platinum 8562Y+ Processor
Intel® Xeon® Platinum 8568Y+ Processor
Intel® Xeon® Platinum 8570 Processor
Intel® Xeon® Platinum 8571N Processor
Intel® Xeon® Platinum 8580 Processor
Intel® Xeon® Platinum 8581V Processor
Intel® Xeon® Platinum 8592+ Processor
Intel® Xeon® Platinum 8592V Processor
Intel® Xeon® Platinum 8593Q Processor
Intel® Xeon® Silver 4509Y Processor
Intel® Xeon® Silver 4510 Processor
Intel® Xeon® Silver 4510T Processor
Intel® Xeon® Silver 4514Y Processor
Intel® Xeon® Silver 4516Y+ Processor
```
