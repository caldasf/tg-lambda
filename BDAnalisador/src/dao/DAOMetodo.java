package dao;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Metodo;

public class DAOMetodo {
	public void gravarMetodos (List<Metodo> listaMetodos) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		manager.getTransaction().begin();
		//rever essa parte
		
		for (Metodo met : listaMetodos) {
			manager.persist(met);
		}

		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	}
}
