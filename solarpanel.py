class solarPanel:
    def __init__(self, address, lat, lon, area):
        # input parameters
        self._address = address
        self._area = area

        # fixed parameters
        self._year = 2010
        self._efficiency = 0.22 # standard Si solar panel
        self._pricePerWatt = 3.5 # in $/kWh for a conventional solar panel in standard condition at (1000 W/m^2) ref. https://news.energysage.com/how-much-does-the-average-solar-panel-installation-cost-in-the-u-s/
        self._lifeTime = 20 

        self._lat = lat
        self._lon = lon

        # calculated parameters
        self._pricePer_kWh = self.get_pricePer_kWh()
        self.meanLightIntensity = self.get_meanLightIntensity()
        self.elecPower = self.get_elecPower()
        self.investmentPrice = self.get_investmentPrice()
        self.monthlySaving = self.get_monthlySaving()

    @property
    def meanLightIntensity(self):
        return self.__meanLightIntensity

    @meanLightIntensity.setter
    def meanLightIntensity(self, value):
        self.__meanLightIntensity = value

    @property
    def elecPower(self):
        return self.__elecPower

    @elecPower.setter
    def elecPower(self, value):
        self.__elecPower = value
    
    @property
    def investmentPrice(self):
        return self.__investmentPrice
    
    @investmentPrice.setter
    def investmentPrice(self, value):
        self.__investmentPrice = value

    @property
    def monthlySaving(self):
        return self.__monthlySaving

    @monthlySaving.setter
    def monthlySaving(self, value):
        self.__monthlySaving = value

    def print_report(self):
        print("-----------------")
        print("meanLightIntensity = " + str(self.meanLightIntensity) + "W/m^2 (mean over 24h)")
        print("investmentPrice    = " + str(self.investmentPrice) + "$")
        print("elecPower          = " + str(self.elecPower) + "W (mean over 24h)")
        print("monthlySaving      = " + str(self.monthlySaving) + "$")

    def get_pricePer_kWh(self):
        # use a rough estimate
        return 0.13

    def get_meanLightIntensity(self):
        # rough estimate using an interpolation in the latitude
        return -12.26 * self._lat + 673.17

    def get_elecPower(self):
        return self._area * self.meanLightIntensity * self._efficiency

    def get_investmentPrice(self):
        return self._pricePerWatt * self.elecPower

    def get_monthlySaving(self):
        return -self.investmentPrice/(12.0*self._lifeTime) + (self.elecPower*3600*24*30.4) * (self._pricePer_kWh/(1000*3600))# - investment + (Energy) * ($/Energie)