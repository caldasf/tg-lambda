package entities;

import java.io.Serializable;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.ManyToOne;

@Entity
public class Classe implements Serializable {
	private static final long serialVersionUID = 1L;
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer idClasse;
	
	private Integer idProjeto;
	private String nome;
	
	public Integer getId() {
		return idClasse;
	}
	public void setId(Integer id) {
		this.idClasse = id;
	}
	public Integer getProjeto() {
		return idProjeto;
	}
	public void setProjeto(Integer projeto) {
		this.idProjeto = projeto;
	}
	public String getNome() {
		return nome;
	}
	public void setNome(String nome) {
		this.nome = nome;
	}
}
