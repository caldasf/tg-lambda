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
	@ManyToOne(cascade = CascadeType.ALL)
	private Projeto idProjeto;
	private String nome;
	
	public Integer getId() {
		return idClasse;
	}
	public void setId(Integer id) {
		this.idClasse = id;
	}
	public Projeto getProjeto() {
		return idProjeto;
	}
	public void setProjeto(Projeto projeto) {
		this.idProjeto = projeto;
	}
	public String getNome() {
		return nome;
	}
	public void setNome(String nome) {
		this.nome = nome;
	}
}
