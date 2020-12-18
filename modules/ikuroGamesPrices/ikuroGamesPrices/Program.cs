using System;
using System.Text;
using System.Threading.Tasks;
using HtmlAgilityPack;
using ScrapySharp.Extensions;
using System.Globalization;
using Newtonsoft.Json;
using System.Net.Http;
using System.Net;

namespace ikuroGamesPrices
{
    class Program
    {
        public static float getIkuroGame(string nombre)
        {
            float price = 0;
            string aux;
            HtmlWeb oWeb = new HtmlWeb();
            HtmlAgilityPack.HtmlDocument doc;
            string url = "https://ikurogames.com/?s=" + nombre.Replace(" ", "+").ToLower() + "&post_type=product";
            doc = oWeb.Load(url);
            foreach (var Nodo in doc.DocumentNode.CssSelect("span.price"))
            {
                byte[] bytes = Encoding.ASCII.GetBytes(Nodo.InnerText);
                byte[] byPrecio = Encoding.Convert(Encoding.ASCII, Encoding.UTF8, bytes);
                string precios = Encoding.UTF8.GetString(byPrecio, 0, byPrecio.Length).Replace("&nbsp;", "").Replace("&ndash;", "-").Replace("USD", "").Replace(" ", "");
                if (precios.Length > 10)
                {
                    price = float.Parse(precios.Split('-')[0].Split(';')[1].Replace(".", ""), CultureInfo.InvariantCulture.NumberFormat);
                }
                else if (precios.Length == 8)
                {
                    aux = precios.Split(';')[1];
                    price = float.Parse(aux);
                }
                else
                {
                    price = float.Parse(precios.Split(';')[1].Replace(".", ""), CultureInfo.InvariantCulture.NumberFormat);
                }
                break;
            }
           
            return price;
        }

        private static string getDollar()
        {
            string dollar = "";
            HtmlWeb oWeb = new HtmlWeb();
            WebClient oClient = new WebClient();
            HtmlDocument doc;
            string url;
            url = "https://es.valutafx.com/USD-ARS.htm";
            doc = oWeb.Load(url);
            foreach (var Nodo in doc.DocumentNode.CssSelect("div.rate-value"))
            {
                dollar = Nodo.InnerHtml;
            }
           
            return dollar;
        }

        public static Price mergePrice(string nombre)
        {
            float ars = 0;
            string dollar = "";
            float price = 0;

            Parallel.Invoke(() =>
            {
                ars = getIkuroGame(nombre);
            }, () =>
            {
                dollar= getDollar();
            });

            price = ars / float.Parse(dollar);
            string aux = price.ToString("####0.00");
            Price priceConverted = new Price(nombre, float.Parse(aux));
            return priceConverted;
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

            Console.WriteLine("Proceso IkuroGames");

            Price dataGame = mergePrice(game);

            var json = JsonConvert.SerializeObject(new
            {
                type = "IkuroGames",
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
                    "https://young-harbor-56590.herokuapp.com/setIkuroGamePrice",
                     new StringContent(json, Encoding.UTF8, "application/json"));
            }
        }
    }
}