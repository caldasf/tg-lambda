package dao;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Classe;

public class DAOClasse {
	public void gravarClasse (List<Classe> listaClasses) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		manager.getTransaction().begin();
		
		//rever essa parte
		if (listaClasses != null) {
			listaClasses = manager.merge(listaClasses);
		}
		
		for (Classe classe : listaClasses) {
			manager.persist(classe);
		}
		
		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	}
}
