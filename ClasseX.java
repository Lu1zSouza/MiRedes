public class ClasseX {
	// A instância da classe deve ser estática, ou seja, se refere a
	// uma pripriedade que dispença o instanciamento para ser acessada.
	private static ClasseX instance;

	//Todos os construtores devem ser privados.
	private ClasseX(){
	};

	//O método único de acesso a instância singular da classe deve ser estático,
	//ou seja, não requer instanciamento para ser acessado.
	public static ClasseX getInstance() {
		if (instance == null) { //verifica se já existe o instanciamento da classe.
			instance = new ClasseX(); //caso não haja, cria um
		}
		return instance; //retorna instância singular da classe
	}
}