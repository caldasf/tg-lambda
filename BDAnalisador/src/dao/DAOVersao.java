package dao;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Versao;

public class DAOVersao {

	public void gravarVersao (Versao versao) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		manager.getTransaction().begin();
		manager.persist(versao);
		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	}
}
