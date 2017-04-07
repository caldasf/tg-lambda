package entities;

import java.io.Serializable;
import java.sql.Date;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Versao implements Serializable {
	private static final long serialVersionUID = 1L;
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer idVersao;
	private Integer idProjeto;
	private String numVersao;
	private Date data;
	
	public Date getData() {
		return data;
	}
	public void setData(Date data) {
		this.data = data;
	}
	public Integer getId() {
		return idVersao;
	}
	public void setId(Integer id) {
		this.idVersao = id;
	}
	public Integer getProjeto() {
		return idProjeto;
	}
	public void setProjeto(Integer projeto) {
		this.idProjeto = projeto;
	}
	public String getNumVersao() {
		return numVersao;
	}
	public void setNumVersao(String numVersao) {
		this.numVersao = numVersao;
	}
}
