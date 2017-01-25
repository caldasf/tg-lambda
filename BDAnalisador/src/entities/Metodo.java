package entities;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Transient;

@Entity
public class Metodo implements Serializable {
	private static final long serialVersionUID = 1L;
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer idMetodo;
	private String nome;
	private Integer qtdLambda;
	private Integer qtdForEach;
	private Integer qtdAic;
	private Integer qtdFilter;
	private Integer qtdMaps;
	private Integer idClasse;
	
	@Transient private Integer linhaInicio;
	@Transient private Integer linhaFim;
	@Transient private String nomeClasse;
	
	public Integer getIdMetodo() {
		return idMetodo;
	}
	public void setIdMetodo(Integer idMetodo) {
		this.idMetodo = idMetodo;
	}
	public String getNomeClasse() {
		return nomeClasse;
	}
	public void setNomeClasse(String nomeClasse) {
		this.nomeClasse = nomeClasse;
	}
	public Integer getIdClasse() {
		return idClasse;
	}
	public void setIdClasse(Integer idClasse) {
		this.idClasse = idClasse;
	}
	public static long getSerialversionuid() {
		return serialVersionUID;
	}
	public Integer getClasse() {
		return idClasse;
	}
	public void setClasse(Integer classe) {
		this.idClasse = classe;
	}
	public Integer getLinhaInicio() {
		return linhaInicio;
	}
	public void setLinhaInicio(Integer linhaInicio) {
		this.linhaInicio = linhaInicio;
	}
	public Integer getLinhaFim() {
		return linhaFim;
	}
	public void setLinhaFim(Integer linhaFim) {
		this.linhaFim = linhaFim;
	}
	public Integer getId() {
		return idMetodo;
	}
	public void setId(Integer id) {
		this.idMetodo = id;
	}
	public String getNome() {
		return nome;
	}
	public void setNome(String nome) {
		this.nome = nome;
	}
	public Integer getQtdLambda() {
		return qtdLambda;
	}
	public void setQtdLambda(Integer qtdLambda) {
		this.qtdLambda = qtdLambda;
	}
	public Integer getQtdForEach() {
		return qtdForEach;
	}
	public void setQtdForEach(Integer qtdForEach) {
		this.qtdForEach = qtdForEach;
	}
	public Integer getQtdAic() {
		return qtdAic;
	}
	public void setQtdAic(Integer qtdAic) {
		this.qtdAic = qtdAic;
	}
	public Integer getQtdFilter() {
		return qtdFilter;
	}
	public void setQtdFilter(Integer qtdFilter) {
		this.qtdFilter = qtdFilter;
	}
	public Integer getQtdMaps() {
		return qtdMaps;
	}
	public void setQtdMaps(Integer qtdMaps) {
		this.qtdMaps = qtdMaps;
	}
}
