from extract_data import extract_product
urls = [
    "https://www.amazon.es/LG-43UR73006LA-Procesador-Potencia-Assistant/dp/B0BYKFCYDV/?_encoding=UTF8&_ref=dlx_gate_sd_dcl_tlt_7d644db1_dt&pd_rd_w=zHFfO&content-id=amzn1.sym.af0bd287-737e-4e81-8dea-869bad051212&pf_rd_p=af0bd287-737e-4e81-8dea-869bad051212&pf_rd_r=42D3W3BAMFS1G6V9SM1K&pd_rd_wg=kZNi8&pd_rd_r=2bf62b1d-17b3-43e8-b267-a4d7a3857702&ref_=pd_gw_unk",
    # "https://www.amazon.es/Vans-Atwood-Zapatillas-Hombre-Canvas/dp/B00CWB45T2/ref=sr_1_2?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=FMBRZIUXXYIA&keywords=vans%2Bhombre&qid=1693657250&sprefix=vans%2Bhombre%2Caps%2C120&sr=8-2&th=1&psc=1",
    # "https://www.amazon.es/dp/B07VDLG8LR/?coliid=I15O16MQ01E07N&colid=22XSMB82WM2B9&ref_=list_c_wl_lv_ov_lig_dp_it&th=1&psc=1",
    "https://www.amazon.es/Xiaomi-System-AX3000-2-Pack-Negro/dp/B09MW2CT7B/?_encoding=UTF8&pd_rd_w=LfTkE&content-id=amzn1.sym.7b21de84-4f5a-439a-98db-74d0a90b0339&pf_rd_p=7b21de84-4f5a-439a-98db-74d0a90b0339&pf_rd_r=6FKAA6Q5YE1WT373AH9H&pd_rd_wg=gaQIt&pd_rd_r=527ec9d2-46c3-4bf9-8365-c073d14336d3&ref_=pd_gw_pd_pss_gwp_d_0&th=1",
]

if __name__ == "__main__":
    for url in urls:
        resultado = extract_product(url)
        print(resultado)