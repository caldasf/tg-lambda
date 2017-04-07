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
	private Long idClasse;
	
	private Integer idVersao;
	private String nome;
	
	public Long getId() {
		return idClasse;
	}
	public void setId(Long id) {
		this.idClasse = id;
	}
	public Integer getVersao() {
		return idVersao;
	}
	public void setVersao(Integer versao) {
		this.idVersao = versao;
	}
	public String getNome() {
		return nome;
	}
	public void setNome(String nome) {
		this.nome = nome;
	}
}
