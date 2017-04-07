//package dao;
//
//import java.io.IOException;
//import java.nio.charset.StandardCharsets;
//import java.nio.file.Files;
//import java.nio.file.Paths;
//
//import javax.persistence.EntityManager;
//import javax.persistence.EntityManagerFactory;
//import javax.persistence.Persistence;
//import javax.persistence.Query;
//
//public class DAOBanco {
//
//	public void inicializarBanco (String path) throws IOException {
//		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
//		EntityManager manager = factory.createEntityManager();
//		String sqlScript = path + "/import_db.sql";
//		
//		String contents = new String(Files.readAllBytes(Paths.get(sqlScript)));
//		
//		Query q = manager.createNativeQuery("BEGIN " + contents + " END;");
//		q.executeUpdate();
//		manager.close();
//	    factory.close();
//	}
//}