ALTER TABLE `Classe`
  ADD CONSTRAINT `Classe_fk_Versao` 
    FOREIGN KEY (`idVersao`)
    REFERENCES `Versao` (`idVersao`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT;


ALTER TABLE `Metodo`
  ADD CONSTRAINT `Metodo_fk_Classe` 
    FOREIGN KEY (`idClasse`)
    REFERENCES `Classe` (`idClasse`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT;

ALTER TABLE `Versao`
  ADD CONSTRAINT `Versao_fk_Projeto` 
    FOREIGN KEY (`idProjeto`)
    REFERENCES `Projeto` (`idProjeto`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT;
