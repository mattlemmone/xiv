#pragma once
template<typename T>
class Singleton {
public:
	// Get singleton

	static T* Singleton::instance() {
		if (!p_instance)
			p_instance = new T;
		return p_instance;
	}
protected:
	Singleton() {}
	~Singleton() {
		delete p_instance;
	}
private:
	static T *p_instance;
};

template <class T> 
T* Singleton<T>::p_instance = nullptr;
