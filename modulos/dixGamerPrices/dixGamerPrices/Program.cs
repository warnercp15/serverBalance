using System;
using System.Text;
using System.Threading.Tasks;
using HtmlAgilityPack;
using ScrapySharp.Extensions;
using Newtonsoft.Json;
using System.Net.Http;

namespace dixGamerPrices
{
    class Program
    {
        public static float getDixGamerGame(string nombre)
        {
            float price = 0;
            Boolean oferta = false;
            string resultado, auxPrice;
            HtmlWeb oWeb = new HtmlWeb();
            HtmlAgilityPack.HtmlDocument doc;
            string url = "http://dixgamer.com/shop/juegos/ps4/accion-ps4/" + nombre.Replace(" ", "-") + "/?v=1d7b33fc26ca";
            doc = oWeb.Load(url);
            foreach (var Nodo in doc.DocumentNode.CssSelect("p.price"))
            {
                foreach (var Nodo2 in doc.DocumentNode.CssSelect("div.product-images span.onsale"))
                {
                    oferta = true;
                    break;
                }
                byte[] bytes = Encoding.ASCII.GetBytes(Nodo.InnerText);
                byte[] byPrecio = Encoding.Convert(Encoding.ASCII, Encoding.UTF8, bytes);
                string[] precios = Encoding.UTF8.GetString(byPrecio, 0, byPrecio.Length).Replace("&nbsp;", "").Replace("&ndash;", "-").Replace("USD", "").Replace(" ", "").Split('-');
                resultado = precios[0].Split('\n')[1];
                if (resultado.Length > 5)
                {
                    auxPrice = "" + resultado[4] + resultado[5] + resultado[6] + resultado[7];
                    price = float.Parse(auxPrice);
                }
                else
                {
                    price = float.Parse(resultado);
                }
                break;
            }
            if (oferta)
            {
                price = price * -1;
            }
            return price;
        }

        static async Task Main(string[] args)
        {
            string game = "";

            if (args.Length > 0)
            {

                foreach (var arg in args)
                {
                    game = arg;
                }
                game=game.Replace("-", " ");
            }
            else
            {
                game = "borderlands 3";
            }

            Console.WriteLine("Proceso DixGamer");

            Price dataGame = new Price(game, getDixGamerGame(game));

            var json = JsonConvert.SerializeObject(new
            {
                type = "dixGamerPrices",
                date = DateTime.UtcNow.ToString("dd-MM-yyyy") + "$" + DateTime.Now.TimeOfDay,
                data = dataGame
            });

            await SendJsonAsync(json);
            Console.WriteLine("Proceso exitoso!\n");
        }

        public static async Task SendJsonAsync(string json)
        {
            using (var client = new HttpClient())
            {
                var response = await client.PostAsync(
                    "http://localhost:5000/setDixGamerPrice",
                     new StringContent(json, Encoding.UTF8, "application/json"));
            }
        }
    }
}
